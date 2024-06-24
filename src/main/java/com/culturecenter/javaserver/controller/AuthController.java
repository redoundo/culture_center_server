package com.culturecenter.javaserver.controller;

import com.culturecenter.javaserver.auth.JwtProvider;
import com.culturecenter.javaserver.dto.*;
import com.culturecenter.javaserver.entity.Users;
import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.service.ChangeService;
import com.culturecenter.javaserver.service.SelectService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Map;

/**
 * 로그인 회원가입과 관련된 요청 처리
 */
@RequiredArgsConstructor
@Controller
@RequestMapping("/api/auth")
public class AuthController {
    private final WebClient webClient = WebClient.create();
    private final JwtProvider jwtProvider;
    private final ChangeService changeService;
    private final SelectService selectService;
    private final BCryptPasswordEncoder passwordEncoder;

    /**
     * access token 을 받아온다.
     * @param sns naver || google
     * @param query access token 을 받아올 때 필요한 내용
     * @return 받아온 내용 반환
     */
    @PostMapping("/{sns}/login")
    @ResponseBody
    public SnsJwtDto snsAccessToken(@PathVariable("sns") String sns, @RequestBody Map<String, Object> query) {
        if (sns == null) throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
        if (sns.equals("naver")) {
            String publishUrl = "https://nid.naver.com/oauth2.0/token";
            return this.webClient.get()
                    .uri(publishUrl + "?" + query.get("query").toString())
                    .retrieve()
                    .bodyToMono(NaverJwtDto.class)
                    .block();
        }
        String publishUrl = "https://oauth2.googleapis.com/token";
        return this.webClient.post()
                .uri(publishUrl)
                .bodyValue(query.get("query"))
                .retrieve()
                .bodyToMono(GoogleJwtDto.class)
                .block();
    }

    /**
     * 네이버 sns 로그인 시, access token 을 사용해  사용자 정보 반환.
     * @param auth Authorization 값
     * @return 사용자 정보 반환.
     */
    @PostMapping("naver/user_info")
    @ResponseBody
    public NaverUserDto naverGetUserInfo (@RequestBody Map<String, String> auth) {
        String url = "https://openapi.naver.com/v1/nid/me";
        String authorization = auth.get("Authorization");
        return this.webClient.get()
                .uri(url)
                .header("Authorization", "Bearer " +  authorization)
                .retrieve()
                .bodyToMono(NaverUserDto.class)
                .block();
    }

    @PostMapping("/signin/{sns}/publish_jwt")
    @ResponseBody
    public JwtDto signInPublishJwt (@PathVariable("sns") String sns,  @RequestBody Map<String, Object> query){
        if (sns == null) throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
        if(query.get("email") == null && query.get("id") == null )
            throw new CustomRuntimeException(ErrorCode.FAILED_AUTHORIZED_EXCEPTION);

        String email = sns.equals("CultureCenters")? null : query.get("email").toString();
        String id = query.get("id").toString();
        try {
            Boolean exist = false;
            if (sns.equals("CultureCenters")) exist = this.selectService.checkUserExist(id, sns);
            else exist = this.selectService.checkUserExist(email, sns);

            if (exist) {
                Users users;

                if (sns.equals("CultureCenters")) users = this.selectService.selectUserInfo(null, id);
                else users = this.selectService.selectUserInfo(null, email);

                JwtDto jwt =  this.jwtProvider.returnJwt(users);
                Authentication authentication = jwtProvider.getAuthentication(jwt.getAccessToken());
                SecurityContextHolder.getContext().setAuthentication(authentication);
                return jwt;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        if (sns.equals("CultureCenters")) {
            LocalDate now = LocalDate.now(ZoneId.of("Asia/Seoul"));
            String password = query.get("password").toString();
            String encodedPassword = this.passwordEncoder.encode(password);
            String providerId = sns.toLowerCase() + "_" + now.getYear() +  "_" + now.getMonthValue()  + "_" + now.getDayOfMonth() + "_" + id;
            String nickname = query.get("nickname").toString();
            SignInInfoDto users = SignInInfoDto.builder()
                    .snsProvider("CultureCenters")
                    .snsProviderId(providerId)
                    .email(id)
                    .password(encodedPassword)
                    .nickname(nickname)
                    .build();
            Users savedUser = this.changeService.signInUser(users);
            JwtDto jwt = this.jwtProvider.returnJwt(savedUser);
            Authentication authentication = jwtProvider.getAuthentication(jwt.getAccessToken());
            SecurityContextHolder.getContext().setAuthentication(authentication);
            return jwt;
        }

        String providerId = sns.toUpperCase() + "_" + id;
        SignInInfoDto infoDto = SignInInfoDto.builder()
                .email(email)
                .nickname(email)
                .password(this.passwordEncoder.encode(providerId))
                .snsProvider(sns)
                .snsProviderId(providerId)
                .build();
        Users users = this.changeService.signInUser(infoDto);
        JwtDto jwt = this.jwtProvider.returnJwt(users);
        Authentication authentication = jwtProvider.getAuthentication(jwt.getAccessToken());
        SecurityContextHolder.getContext().setAuthentication(authentication);
        return jwt;
    }

    /**
     * 로그인시 jwt 토큰 발행
     * @param sns 로그인하는 방법  naver || google || culturecenters(자체 로그인)
     * @param query 로그인에 필요한 내용
     * @return jwt 토큰
     */
    @PostMapping("/login/{sns}/publish_jwt")
    public ResponseEntity<JwtDto> loginPublishJwt (@PathVariable("sns") String sns, @RequestBody Map<String, Object> query) {
        if (sns == null) throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
        if(query.get("email") == null && query.get("id") == null )
            throw new CustomRuntimeException(ErrorCode.FAILED_AUTHORIZED_EXCEPTION);

        String id = query.get("id").toString();
        String email = sns.equals("CultureCenters")? null : query.get("email").toString();
        try {
            Boolean exist = false;
            if (sns.equals("CultureCenters")) exist = this.selectService.checkUserExist(id, sns);
            else  exist = this.selectService.checkUserExist(email, sns);

            if (!exist) throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
        }

        Users user;
        if (sns.equals("CultureCenters")) user = this.selectService.selectUserInfo(null, id);
        else user = this.selectService.selectUserInfo(null, email);

        JwtDto jwt = this.jwtProvider.returnJwt(user);
        Authentication authentication = jwtProvider.getAuthentication(jwt.getAccessToken());
        SecurityContextHolder.getContext().setAuthentication(authentication);
        return ResponseEntity.status(200).body(jwt);
    }

    /**
     * 닉네임이 겹치는지 확인
     * @param map 닉네임
     * @return 유효성 여부
     */
    @PostMapping("/signin/check_nickname_is_unique")
    @ResponseBody
    public Boolean nicknameUniqueness(@RequestBody Map<String, String> map) {
        if(map == null || map.get("nickname") == null)
            throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);

        return this.selectService.checkNicknameUniqueness(map.get("nickname"));
    }


}
