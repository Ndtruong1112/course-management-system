package com.mkii.coursemanagementsystem.specification;

import jakarta.persistence.criteria.*;
import org.springframework.data.jpa.domain.Specification;

public class GenericSpecification<T> implements Specification<T> {

    private final SearchCriteria criteria;

    public GenericSpecification(SearchCriteria criteria) {
        this.criteria = criteria;
    }

    public SearchCriteria getCriteria() {
        return criteria;
    }

    @Override
    public Predicate toPredicate(Root<T> root, CriteriaQuery<?> query, CriteriaBuilder builder) {
        if (criteria == null || criteria.getKey() == null) {
            return null;
        }

        Path<?> path;
        try {
            path = root.get(criteria.getKey());
        } catch (IllegalArgumentException e) {
            return null; // Field does not exist on entity
        }

        String operation = criteria.getOperation();
        Object value = criteria.getValue();
        if (value == null) {
            return null;
        }

        String strValue = value.toString();
        Class<?> javaType = path.getJavaType();

        switch (operation) {
            case ">":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.gt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case ">=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.ge(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.lt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.le(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "!":
            case "!=":
                if (javaType == String.class) {
                    return builder.notLike(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                }
                Object castVal = castToRequiredType(javaType, strValue);
                return castVal != null ? builder.notEqual(path, castVal) : null;

            case ":":
            default:
                if (javaType == String.class) {
                    return builder.like(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                } else {
                    Object eqVal = castToRequiredType(javaType, strValue);
                    return eqVal != null ? builder.equal(path, eqVal) : null;
                }
        }
        return null;
    }

    private Number parseNumber(Class<?> targetType, String str) {
        try {
            if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            }
            return Double.parseDouble(str);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Object castToRequiredType(Class<?> targetType, String str) {
        try {
            if (targetType == String.class) {
                return str;
            } else if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            } else if (targetType == Boolean.class || targetType == boolean.class) {
                return Boolean.parseBoolean(str);
            }
            return str;
        } catch (Exception e) {
            return null;
        }
    }
}
