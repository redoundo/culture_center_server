package com.culturecenter.javaserver.auth;

import com.culturecenter.javaserver.dto.JwtDto;
import com.culturecenter.javaserver.entity.Users;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("auth 관련 테스트")
public class AuthTest {
    private JwtProvider provider = new JwtProvider();

    @Test
    @Disabled
    @DisplayName("jwt 생성 테스트")
    void jwtCreateTest() {
        Users user = Users.builder()
                .userId(2)
                .email("cultureCenterId")
                .password("$2a$10$hE7vWjx3JSTUe3kQdTL2tOiJHV59rkbRKVnSE0eHHyw2zEsqAoea2")
                .snsProvider("CultureCenters")
                .snsProviderId("culturecenters_2024_07_13_cultureCenterId")
                .build();
//        Users user = Users.builder()
//                .userId(1)
//                .email("park822435@naver.com")
//                .snsProvider("naver")
//                .snsProviderId("NAVER_gM15REiQF5yUV4LmJ4uYyvBsuTePQAnZ_P_Is5P6ONs")
//                .password("1208961f642fbc74a0eb201a49621381e7ede60162e0612d0f693c781c6792af")
//                .nickname("박혜린")
//                .build();
        JwtDto dto = provider.returnJwt(user);
        System.out.println(dto.getAccessToken());
        assertNotNull(dto);
    }

}
