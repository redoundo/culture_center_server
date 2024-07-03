package com.culturecenter.javaserver.dto;

import com.culturecenter.javaserver.entity.Lectures;
import lombok.*;

import java.util.List;

/**
 * 총 강좌 수를 포함한 강좌 내용.
 */
@Getter
@Setter
@Builder
@RequiredArgsConstructor
@AllArgsConstructor
public class SearchResultsDto {
    private List<Lectures> lectures;
    private Integer total;
}
