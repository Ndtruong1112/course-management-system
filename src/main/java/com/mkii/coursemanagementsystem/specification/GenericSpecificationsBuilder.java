package com.mkii.coursemanagementsystem.specification;

import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class GenericSpecificationsBuilder<T> {

    private final List<SearchCriteria> params = new ArrayList<>();

    public GenericSpecificationsBuilder<T> with(String key, String operation, Object value) {
        params.add(new SearchCriteria(key, operation, value));
        return this;
    }

    public GenericSpecificationsBuilder<T> with(SearchCriteria criteria) {
        params.add(criteria);
        return this;
    }

    public GenericSpecificationsBuilder<T> withSearchQuery(String search) {
        if (search == null || search.trim().isEmpty()) {
            return this;
        }
        // Match patterns: key>=val, key<=val, key!=val, key>val, key<val, key:val, key!val separated by comma
        Pattern pattern = Pattern.compile("([a-zA-Z0-9_.]+?)(>=|<=|!=|!|:|>|<)([a-zA-Z0-9_.@\\s\\p{L}-]+?)(?:,|$)");
        Matcher matcher = pattern.matcher(search);
        while (matcher.find()) {
            String key = matcher.group(1).trim();
            String op = matcher.group(2).trim();
            String value = matcher.group(3).trim();
            with(key, op, value);
        }
        return this;
    }

    public Specification<T> build() {
        if (params.isEmpty()) {
            return null;
        }

        Specification<T> result = new GenericSpecification<>(params.get(0));
        for (int i = 1; i < params.size(); i++) {
            result = Specification.where(result).and(new GenericSpecification<>(params.get(i)));
        }
        return result;
    }
}
