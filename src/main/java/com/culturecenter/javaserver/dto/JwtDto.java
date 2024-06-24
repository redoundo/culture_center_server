package com.culturecenter.javaserver.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.Date;

/**
 * 직접 생성해 반환하는 jwt 토큰
 */
@Builder
@Getter
public class JwtDto {
    private String accessToken;
    private String refreshToken;
    private String grantType;
    private Date accessTokenExpiredAt;
}
