package com.culturecenter.javaserver.dto;

import lombok.*;

/**
 * 강좌 상태 확인을 할 때 사용되는 id 와 url 보유
 */
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class ForScrapDto {
    private Integer lectureId;
    private String url;
}
