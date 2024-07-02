package com.culturecenter.javaserver.dto;

import lombok.*;

@Builder
@Getter
@Setter
@RequiredArgsConstructor
@AllArgsConstructor
public class NaverUserDto {
    private String resultCode;
    private String message;
    private NaverUserInfoDto response;
}
