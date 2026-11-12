import os
import re
from collections import Counter


class CodebaseRAG:
    """
    Lightweight local Retrieval-Augmented Generation (RAG) engine indexing the real Java/Spring Boot
    codebase under src/main so both Local Qwen-3B + LoRA and Cloud models answer with exact facts
    and zero hallucination.
    """

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.docs = []
        self.refresh()

    def refresh(self):
        self.docs = []
        src_java = os.path.join(self.root_dir, "src", "main", "java")
        app_props = os.path.join(self.root_dir, "src", "main", "resources", "application.properties")

        if os.path.exists(src_java):
            for root, _, files in os.walk(src_java):
                for fname in sorted(files):
                    if not fname.endswith(".java"):
                        continue
                    full_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(full_path, self.root_dir).replace("\\", "/")
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().strip()
                        if content:
                            self.docs.append(self._build_doc(rel_path, fname, content, is_doc=False))
                    except Exception:
                        pass

        if os.path.exists(app_props):
            rel_path = os.path.relpath(app_props, self.root_dir).replace("\\", "/")
            try:
                with open(app_props, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                if content:
                    self.docs.append(self._build_doc(rel_path, "application.properties", content, is_doc=False))
            except Exception:
                pass

        # Index concise sections from README.md and project architecture reference docs
        md_sources = []
        readme_path = os.path.join(self.root_dir, "README.md")
        if os.path.exists(readme_path):
            md_sources.append(readme_path)
        refs_dir = os.path.join(self.root_dir, ".agents", "skills", "cms-standards", "references")
        if os.path.exists(refs_dir):
            for fname in sorted(os.listdir(refs_dir)):
                if fname.endswith(".md"):
                    md_sources.append(os.path.join(refs_dir, fname))

        for md_path in md_sources:
            rel_path = os.path.relpath(md_path, self.root_dir).replace("\\", "/")
            try:
                with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_md = f.read().strip()
                for sec_title, sec_body in self._split_markdown_sections(raw_md):
                    if len(sec_body) >= 80:
                        label = f"{rel_path}#{sec_title}"
                        self.docs.append(self._build_doc(label, sec_title, sec_body, is_doc=True))
            except Exception:
                pass

        return len(self.docs)

    @staticmethod
    def _split_markdown_sections(md_text):
        sections = []
        cur_title = "Overview"
        cur_lines = []
        for line in md_text.splitlines():
            if line.startswith("## "):
                body = "\n".join(cur_lines).strip()
                if body:
                    sections.append((cur_title, body[:1400]))
                cur_title = re.sub(r"[^a-zA-Z0-9À-ỹ_-]+", "-", line[3:].strip()).strip("-") or "Section"
                cur_lines = [line]
            else:
                cur_lines.append(line)
        body = "\n".join(cur_lines).strip()
        if body:
            sections.append((cur_title, body[:1400]))
        return sections

    def _build_doc(self, rel_path, fname, content, is_doc=False):
        class_name = os.path.splitext(fname)[0]
        tokens = self._tokenize(rel_path + " " + content)
        return {
            "path": rel_path,
            "name": fname,
            "class_name": class_name,
            "class_lower": class_name.lower(),
            "content": content,
            "content_lower": content.lower(),
            "is_doc": is_doc,
            "tf": Counter(tokens),
        }

    @staticmethod
    def _tokenize(text):
        # Split CamelCase & snake_case so 'findByPriceRange' matches 'price', 'range', 'findbypricerange'
        expanded = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
        raw_tokens = re.findall(r"[a-zA-Z0-9_À-ỹ/.-]+", expanded.lower())
        result = []
        for tok in raw_tokens:
            result.append(tok)
            if "_" in tok or "/" in tok or "." in tok:
                for sub in re.split(r"[_/.]+", tok):
                    if len(sub) >= 2:
                        result.append(sub)
        return [t for t in result if len(t) >= 2]

    @staticmethod
    def is_code_generation_query(query):
        q = query.lower()
        markers = [
            "viết", "tạo", "module", "entity", "dao", "dto", "service",
            "controller", "cấu trúc", "scaffold", "triển khai", "thêm chức năng"
        ]
        return any(m in q for m in markers)

    _STOPWORDS = {
        "của", "với", "trong", "không", "cho", "được", "các", "là", "nào", "khi", "như", "thế",
        "hay", "hoặc", "gì", "này", "một", "những", "bằng", "cách", "trên", "dưới", "qua", "tại",
        "file", "java", "class", "public", "private", "protected", "static", "final", "void",
        "return", "string", "long", "boolean", "list", "system", "course", "management",
        "hệ", "thống", "dự", "án", "lớp", "trường", "bảng", "cơ", "sở", "dữ", "liệu", "làm",
        "để", "bị", "về", "sẽ", "có", "tên", "gồm", "chính", "ngoài", "bản", "ghi", "mới", "cũ",
    }

    def retrieve(self, query, top_k=4, max_chars=2400):
        if not self.docs or not query:
            return []

        q_lower = query.lower()
        q_tokens = [t for t in self._tokenize(query) if t not in self._STOPWORDS]
        scored = []

        # Synonym/Vietnamese-to-Java domain hints so Vietnamese questions find exact Java classes
        domain_boosts = {
            "tài liệu": ["documentserviceimpl", "document"],
            "minio": ["miniostorageservice", "documentserviceimpl", "document", "minioconfig"],
            "nhị phân": ["miniostorageservice", "documentserviceimpl", "document"],
            "vật lý": ["miniostorageservice", "documentserviceimpl", "document"],
            "pdf": ["miniostorageservice", "documentserviceimpl", "document"],
            "docx": ["miniostorageservice", "documentserviceimpl", "document"],
            "version": ["documentserviceimpl", "document"],
            "phiên bản": ["documentserviceimpl", "document"],
            "trùng tên": ["documentserviceimpl", "document"],
            "false": ["documentserviceimpl", "document"],
            "xóa mềm": ["documentserviceimpl", "document"],
            "không bị mất": ["documentserviceimpl", "document"],
            "khóa ngoại": ["document", "student", "department"],
            "documents": ["document", "documentserviceimpl"],
            "khóa học": ["course", "coursedaoimpl", "courserequestdto"],
            "mở rộng": ["coursedaoimpl", "studentdaoimpl", "departmentdaoimpl"],
            "truy vấn": ["coursedaoimpl", "hibernatepaginationsortingdao"],
            "giá": ["coursedaoimpl", "course"],
            "sinh viên": ["student", "studentdaoimpl", "studentrequestdto"],
            "duy nhất": ["student", "department", "user"],
            "unique": ["student", "department", "user"],
            "khoa": ["department", "departmentdaoimpl"],
            "dao cha": ["hibernatepaginationsortingdao", "hibernategenericdao"],
            "lớp cha": ["hibernatepaginationsortingdao", "hibernategenericdao"],
            "tổng quát": ["hibernatepaginationsortingdao", "hibernategenericdao"],
            "phân trang": ["hibernatepaginationsortingdao", "hibernategenericdao"],
            "sắp xếp": ["hibernatepaginationsortingdao"],
            "url": ["apiconstants", "courserest", "studentrest", "documentrest"],
            "endpoint": ["apiconstants", "courserest", "studentrest", "documentrest"],
            "bảo mật": ["securityconfig", "jwttokenprovider", "aesutil", "aesencryptconverter"],
            "jwt": ["securityconfig", "jwttokenprovider", "jwtauthenticationfilter"],
            "mã hóa": ["aesutil", "aesencryptconverter", "securityserviceimpl"],
            "specification": ["genericspecification", "genericspecificationsbuilder"],
            "lọc": ["genericspecification", "genericspecificationsbuilder"],
        }

        boosted_names = set()
        for phrase, targets in domain_boosts.items():
            if phrase in q_lower:
                boosted_names.update(targets)

        is_codegen = self.is_code_generation_query(query)
        if is_codegen:
            boosted_names.update(["hibernatepaginationsortingdao", "coursedaoimpl", "course", "courserequestdto", "apiconstants"])

        for doc in self.docs:
            score = 0.0
            if doc["class_lower"] in q_lower:
                score += 40.0
            if doc["class_lower"] in boosted_names:
                score += 18.0
            if doc["class_lower"] == "hibernatepaginationsortingdao" and ("phân trang" in q_lower or "sắp xếp" in q_lower):
                score += 25.0
            if doc["class_lower"] == "miniostorageservice" and ("vật lý" in q_lower or "nhị phân" in q_lower or "lưu ở đâu" in q_lower):
                score += 22.0
            # Keep Java files primary during code generation; allow architecture markdown on Q&A queries
            if doc.get("is_doc"):
                if is_codegen:
                    score -= 12.0
                else:
                    if "metadata" in doc["content_lower"] and ("cơ sở dữ liệu" in q_lower or "nhị phân" in q_lower or "vật lý" in q_lower or "minio" in q_lower):
                        score += 20.0
            # De-prioritize boilerplate constant/main files unless directly referenced
            if doc["class_lower"] in ("messageconstants", "coursemanagementsystemapplication") and doc["class_lower"] not in q_lower:
                score -= 10.0

            for tok in q_tokens:
                if tok in doc["tf"]:
                    score += min(doc["tf"][tok], 4) * 1.5
                if tok in doc["class_lower"]:
                    score += 7.0

            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = []
        used_chars = 0

        for idx, (_, doc) in enumerate(scored[:top_k]):
            remaining = max_chars - used_chars
            if remaining < 320 and selected:
                break
            # Allow the #1 primary match up to ~62% of the budget so complete classes like CourseDaoImpl fit intact
            target_limit = int(max_chars * 0.62) if idx == 0 else max(450, remaining)
            per_limit = min(remaining - 40, target_limit) if selected else min(max_chars - 40, target_limit)
            snippet = self._compact_snippet(
                doc["content"],
                query_tokens=q_tokens,
                query_lower=q_lower,
                per_file_limit=max(320, per_limit),
            )
            entry = f"// File: {doc['path']}\n{snippet}"
            selected.append({"path": doc["path"], "class_name": doc["class_name"], "snippet": entry})
            used_chars += len(entry) + 2

        return selected

    @staticmethod
    def _compact_snippet(content, query_tokens=None, query_lower="", per_file_limit=1200):
        """Strip boilerplate imports/loggers and extract the highest-signal window matching the query."""
        body_lines = []
        for raw in content.splitlines():
            s = raw.strip()
            if s.startswith("import ") or s.startswith("private static final Logger"):
                continue
            if s == "" and (not body_lines or body_lines[-1] == ""):
                continue
            body_lines.append(raw)

        full_body = "\n".join(body_lines).strip()
        if len(full_body) <= per_file_limit:
            return full_body

        # Keep class signature header plus the best-matching method/field window
        header_lines = []
        start_body_idx = 0
        for idx, line in enumerate(body_lines):
            header_lines.append(line)
            start_body_idx = idx + 1
            if "{" in line or len(header_lines) >= 6:
                break
        header_text = "\n".join(header_lines)

        rest_lines = body_lines[start_body_idx:]
        if not rest_lines:
            return full_body[:per_file_limit] + "\n// ..."

        toks = {t for t in (query_tokens or []) if len(t) >= 3}
        q_low = query_lower or ""
        want_version = any(k in q_low for k in ("version", "phiên bản", "trùng tên", "false", "active"))
        want_soft_delete = any(k in q_low for k in ("xóa", "deleted", "không bị mất", "mềm"))
        want_query = any(k in q_low for k in ("mở rộng", "truy vấn", "tìm", "find", "search", "price", "hql"))

        line_scores = []
        for line in rest_lines:
            l_lower = line.lower()
            sc = 0
            for t in toks:
                if t in l_lower:
                    sc += 2
            if want_version and any(k in l_lower for k in ("setactive(false)", "++versioncount", "tăng số phiên bản", "createdocumentwithnewversion", "setactive(")):
                sc += 30
            if want_soft_delete and any(k in l_lower for k in ("setdeleted(true)", "soft deleting", "public string delete(map")):
                sc += 30
            if want_query and any(k in l_lower for k in ("searchby", "findbypricerange", "findbyhql")):
                sc += 18
            line_scores.append(sc)

        # Slide window over rest_lines maximizing total keyword hits
        best_start = 0
        best_score = -1
        window_size = 22
        for i in range(len(rest_lines)):
            win_sc = sum(line_scores[i:i + window_size])
            if win_sc > best_score:
                best_score = win_sc
                best_start = i

        win_start = max(0, best_start - 3)
        remaining_budget = max(250, per_file_limit - len(header_text) - 20)
        chosen = []
        cur_len = 0
        for line in rest_lines[win_start:]:
            if cur_len + len(line) + 1 > remaining_budget and chosen:
                break
            chosen.append(line)
            cur_len += len(line) + 1

        middle_prefix = "// ...\n" if win_start > 0 else ""
        return f"{header_text}\n{middle_prefix}" + "\n".join(chosen) + "\n// ..."

    def format_context_block(self, query, top_k=4, max_chars=2400):
        hits = self.retrieve(query, top_k=top_k, max_chars=max_chars)
        if not hits:
            return "", []
        files = [h["path"] for h in hits]
        block = (
            "[TÀI LIỆU THAM KHẢO TỪ CODEBASE DỰ ÁN - BÁM SÁT PACKAGE, CLASS, FIELD THẬT]\n"
            + "\n\n".join(h["snippet"] for h in hits)
        )
        return block, files


def classify_eval_task(prompt=""):
    """Phân loại bài toán theo prompt để chọn Rubric chấm điểm chính xác nhất."""
    p = (prompt or "").lower().strip()
    if not p:
        return "dao_module", "Chuẩn Kiến Trúc Enterprise (DAO + Entity)"

    has_dto_kw = any(k in p for k in ("requestdto", "responsedto", "dto", "validation", "@valid", "@notblank", "@notnull"))
    has_dao_kw = any(k in p for k in ("dao", "entitymanager", "hql", "hibernate", "soft delete", "xóa mềm", "findbypricerange", "searchby"))
    has_codegen_verb = any(k in p for k in ("viết", "tạo", "triển khai", "thiết kế", "sinh mã", "implement", "create", "module"))

    if has_dto_kw and not has_dao_kw:
        return "dto_design", "Rubric: Thiết Kế DTO & Validation"

    is_qa = (
        any(k in p for k in ("giải thích", "là gì", "tại sao", "như thế nào", "ở đâu", "lưu cái gì", "cấu trúc bảng", "liên kết"))
        and not any(k in p for k in ("viết", "tạo module", "triển khai cơ chế", "thiết kế lớp"))
    )
    if is_qa:
        return "concept_qa", "Rubric: Hỏi-Đáp Nghiệp Vụ & Codebase"

    is_method_only = (
        ("phương thức" in p or "hàm " in p or "findby" in p or "searchby" in p or "truy vấn" in p)
        and not re.search(r"\bentity\b", p)
        and not re.search(r"\bmodule\b", p)
    )
    if is_method_only and has_dao_kw:
        return "dao_method", "Rubric: Truy Vấn Generic DAO & HQL"

    return "dao_module", "Rubric: Code Module (Entity + Generic DAO)"


def evaluate_architecture_compliance(text, prompt=""):
    """
    Context-aware 5-criteria (100-point) architecture & compatibility scorer
    tailored to the prompt task type (Module DAO, DAO HQL Method, DTO Design, or Codebase Q&A).
    """
    task_type, task_label = classify_eval_task(prompt)
    if not text:
        return {
            "score": 0,
            "passed_count": 0,
            "total": 5,
            "task_type": task_type,
            "task_label": task_label,
            "criteria": [],
        }

    text_lower = text.lower()
    avoids_jpa_repo = (
        "extends jparepository" not in text_lower
        and "extends crudrepository" not in text_lower
        and ": jparepository" not in text_lower
    )
    has_correct_package = (
        "com.mkii.coursemanagementsystem" in text_lower
        or "com.mkii." in text_lower
    )
    has_generic_dao = (
        "hibernatepaginationsortingdao" in text_lower
        or "ipaginationsortingdao" in text_lower
        or "hibernategenericdao" in text_lower
        or "igenericdao" in text_lower
    )
    has_em_hql = (
        "entitymanager" in text_lower
        or "@persistencecontext" in text_lower
        or "findbyhql" in text_lower
        or "createquery" in text_lower
    )
    has_dto_val = any(
        k in text_lower
        for k in ["dto", "requestdto", "responsedto", "@valid", "@notnull", "@notblank", "@size", "@min", "@positiveorzero"]
    )

    if task_type == "dto_design":
        has_req_resp = ("requestdto" in text_lower or "courserequestdto" in text_lower) and (
            "responsedto" in text_lower or "courseresponsedto" in text_lower or "dto" in text_lower
        )
        has_jakarta_val = any(
            k in text_lower for k in ("@notblank", "@notnull", "@min", "@max", "@size", "@positive", "jakarta.validation")
        )
        has_clean_lombok = any(k in text_lower for k in ("@getter", "@setter", "@data", "@builder")) and (
            "@entity" not in text_lower
        ) and avoids_jpa_repo
        has_real_fields = sum(1 for f in ("title", "price", "duration", "description") if f in text_lower) >= 2
        criteria = [
            {"name": "Đúng Package com.mkii.coursemanagementsystem", "passed": bool(has_correct_package), "weight": 20},
            {"name": "Tách biệt RequestDTO & ResponseDTO", "passed": bool(has_req_resp), "weight": 25},
            {"name": "Áp dụng Jakarta Validation (@NotBlank, @NotNull, @Min...)", "passed": bool(has_jakarta_val), "weight": 25},
            {"name": "Chuẩn Lombok & Clean DTO (không lẫn @Entity)", "passed": bool(has_clean_lombok), "weight": 15},
            {"name": "Khớp đúng thuộc tính Course thật (title, price, duration)", "passed": bool(has_real_fields), "weight": 15},
        ]
    elif task_type == "concept_qa":
        has_core_comp = any(
            k in text_lower for k in ("documentserviceimpl", "document", "tbl_document", "hibernatepaginationsortingdao", "coursedaoimpl", "student")
        )
        has_fk_storage = any(
            k in text_lower for k in ("app_detail_fk", "appid", "tbl_document", "minio", "metadata", "unique")
        )
        has_version_soft = any(
            k in text_lower for k in ("active = false", "active=false", "setactive(false)", "version", "++versioncount", "deleted = true", "setdeleted(true)")
        )
        has_dao_align = ("documentdao" in text_lower or "hibernate" in text_lower or "entitymanager" in text_lower or "hql" in text_lower or "idocumentdao" in text_lower)
        criteria = [
            {"name": "Nhận diện đúng Entity / Service / Thành phần thật", "passed": bool(has_core_comp), "weight": 20},
            {"name": "Đúng tên bảng, khóa ngoại & MinIO Storage", "passed": bool(has_fk_storage), "weight": 25},
            {"name": "Đúng logic Versioning / Soft Delete (active=false, version)", "passed": bool(has_version_soft), "weight": 25},
            {"name": "Đúng định hướng tầng DAO / Query của dự án", "passed": bool(has_dao_align), "weight": 15},
            {"name": "Không nhầm sang kiến trúc JpaRepository ngoài luồng", "passed": bool(avoids_jpa_repo), "weight": 15},
        ]
    elif task_type == "dao_method":
        has_dao_pattern = has_generic_dao or "findbyhql" in text_lower or "super." in text_lower or "icoursedao" in text_lower or "coursedaoimpl" in text_lower
        has_real_hql = has_em_hql and any(k in text_lower for k in ("between", ":minprice", ":maxprice", "map.of", "setparameter", "findbyhql"))
        has_real_symbols = "findbypricerange" in text_lower and "course" in text_lower and "price" in text_lower
        has_java_sig = ("@override" in text_lower or "public list<" in text_lower) and ("double" in text_lower or "bigdecimal" in text_lower)
        criteria = [
            {"name": "Tương thích Generic DAO (CourseDaoImpl / findByHql)", "passed": bool(has_dao_pattern), "weight": 25},
            {"name": "Quản lý EntityManager & Truy vấn HQL có tham số", "passed": bool(has_real_hql), "weight": 25},
            {"name": "Không lạm dụng Spring Data JpaRepository", "passed": bool(avoids_jpa_repo), "weight": 20},
            {"name": "Đúng tên hàm, Entity & thuộc tính (findByPriceRange, price)", "passed": bool(has_real_symbols), "weight": 15},
            {"name": "Chuẩn chữ ký Java & kiểu trả về (@Override, List<Course>)", "passed": bool(has_java_sig), "weight": 15},
        ]
    else:
        has_entity_or_dto = has_dto_val or any(
            k in text_lower for k in ("@entity", "@table", "jakarta.persistence", "@getter", "@sqldelete", "deleted = true", "setdeleted(true)")
        )
        criteria = [
            {"name": "Kế thừa Generic DAO (HibernatePaginationSortingDao)", "passed": bool(has_generic_dao), "weight": 25},
            {"name": "Quản lý EntityManager & Dynamic HQL Query", "passed": bool(has_em_hql), "weight": 20},
            {"name": "Không lạm dụng Spring Data JpaRepository", "passed": bool(avoids_jpa_repo), "weight": 20},
            {"name": "Đúng Package com.mkii.coursemanagementsystem", "passed": bool(has_correct_package), "weight": 15},
            {"name": "Chuẩn Entity / DTO & Jakarta Annotations", "passed": bool(has_entity_or_dto), "weight": 20},
        ]

    total_score = sum(c["weight"] for c in criteria if c["passed"])
    passed_count = sum(1 for c in criteria if c["passed"])

    return {
        "score": total_score,
        "passed_count": passed_count,
        "total": len(criteria),
        "task_type": task_type,
        "task_label": task_label,
        "criteria": criteria,
    }
