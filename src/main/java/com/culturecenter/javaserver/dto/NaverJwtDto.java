package com.culturecenter.javaserver.dto;

import lombok.*;
import org.springframework.lang.Nullable;

/**
 * 네이버 로그인이 진행되면서 발급받는 내용
 */
@Builder
@Getter
@Setter
@AllArgsConstructor
public class NaverJwtDto implements SnsJwtDto {
    private @Nullable  String access_token;
    private @Nullable  String refresh_token;
    private @Nullable  String token_type;
    private @Nullable  Integer expires_in;
    private @Nullable String error;
    private @Nullable String error_description;


}
