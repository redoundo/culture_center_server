package com.culturecenter.javaserver.dto;

import lombok.*;

/**
 * 업데이트 가능한 내용. 변경할 것을 대비해 dto 로 전달.
 */
@Getter
@Setter
@Builder
@RequiredArgsConstructor
@AllArgsConstructor
public class UpdatableInfoDto {
    private String nickname;
}
