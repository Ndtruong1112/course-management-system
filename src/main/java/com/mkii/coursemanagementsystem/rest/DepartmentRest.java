package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/api/departments")
public interface DepartmentRest {

    @PostMapping
    ResponseEntity<DepartmentResponseDTO> create(@RequestBody DepartmentRequestDTO dto);

    @PutMapping("/{id}")
    ResponseEntity<DepartmentResponseDTO> update(@PathVariable("id") Long id, @RequestBody DepartmentRequestDTO dto);

    @DeleteMapping("/{id}")
    ResponseEntity<Void> delete(@PathVariable("id") Long id);

    @GetMapping("/{id}")
    ResponseEntity<DepartmentResponseDTO> getById(@PathVariable("id") Long id);

    @GetMapping("/code/{code}")
    ResponseEntity<DepartmentResponseDTO> getByCode(@PathVariable("code") String code);

    @GetMapping
    ResponseEntity<List<DepartmentResponseDTO>> getAll();

    @GetMapping("/search")
    ResponseEntity<List<DepartmentResponseDTO>> search(@RequestParam("keyword") String keyword);
}
