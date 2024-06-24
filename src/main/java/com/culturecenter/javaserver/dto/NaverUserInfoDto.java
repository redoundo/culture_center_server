package com.culturecenter.javaserver.dto;

import lombok.*;

/**
 * 	https://openapi.naver.com/v1/nid/me 에 사용자 정보 요청시 반환되는 내용
 */
@Builder
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class NaverUserInfoDto {
    private String email;
    private String id;
    private String nickname;
    private String name;
    private String gender;
    private String age;
    private String birthday;
    private String birthyear;
    private String profile_image;
    private String mobile;
}
