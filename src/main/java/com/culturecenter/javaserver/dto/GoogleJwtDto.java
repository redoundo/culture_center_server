package com.culturecenter.javaserver.dto;

import lombok.*;
import org.springframework.lang.Nullable;

/**
 * google sns 로그인시 반환하는 내용
 */
@Getter
@Setter
@Builder
@AllArgsConstructor
public class GoogleJwtDto implements SnsJwtDto {
    private @Nullable String access_token;
    private @Nullable  Integer expires_in;
    private @Nullable  String scope;
    private @Nullable  String token_type;
    private @Nullable  String id_token;
    private @Nullable  String refresh_token;
}
