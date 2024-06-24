package com.culturecenter.javaserver.dto;

import lombok.*;

/**
 * 회원 가입시 필요한 내용
 */
@Builder
@Getter
@Setter
@AllArgsConstructor
public class SignInInfoDto {
    private String email;
    private String password;
    private String nickname;
    private String snsProvider;
    private String snsProviderId;
}
