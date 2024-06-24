package com.culturecenter.javaserver.dto;

import lombok.*;
import org.springframework.lang.Nullable;

/**
 * 검색 조건들
 */
@Getter
@Setter
@Builder
@AllArgsConstructor
public class SearchConditions {
    private @Nullable String keyword;
    @Builder.Default
    private @Nullable Integer page = 1;
    @Builder.Default
    private @Nullable String target = "adult";
    private @Nullable String category;
    private @Nullable String centerType;
    private @Nullable String centerName;

    private @Nullable Double latitude;
    private @Nullable Double longitude;
    private @Nullable String address;
}
