package com.culturecenter.javaserver.auth;


import com.culturecenter.javaserver.dto.JwtDto;
import com.culturecenter.javaserver.entity.Users;
import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import io.jsonwebtoken.*;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import javax.crypto.SecretKey;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import static com.culturecenter.javaserver.utils.Util.checking;

/**
 * jwt 발행 및 유효성 확인 기능 포함.
 */
@Component
@RequiredArgsConstructor
public class JwtProvider {
    private final String secret = "cultureCenterServer94cultureCenterServer19cultureCenterServer42";
    private final Integer AccessTokenExpiredAt = 6000000;
    private final Integer RefreshTokenExpiredAt = 70000;
    private final String issuer = "cultureCenterServer";
    private final String header = "Authorization";
    private final String authority = "auth";

    private final SecretKey key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    /**
     * 사용자 아이디로 jwt 토큰 생성.
     * @param user token 에 있는 userId 로 찾아온 사용자 정보.
     * @return 생성된 jwt 토큰
     */
    public JwtDto returnJwt(Users user){

        Long now = new Date(System.currentTimeMillis()).getTime();
        Date accessExpiredAt = new Date(now + AccessTokenExpiredAt);
        String accessToken = Jwts.builder()
                .claims().add("id" , user.getUserId()).add(authority , "ROLE_USER").and()
                .expiration(accessExpiredAt)
                .issuer(issuer)
                .signWith(key)
                .compact();
        String refreshToken = Jwts.builder()
                .expiration(new Date(now + RefreshTokenExpiredAt))
                .signWith(key)
                .compact();

        return JwtDto.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .grantType("bearer")
                .accessTokenExpiredAt(accessExpiredAt)
                .build();
    }
    /**
     * 일단 sns 인증을 진행하고 난 뒤에 회원가입을 진행하므로 토큰이 존재하지 않더라도 계속 진행.
     * @param request accessToken 을 가져올 request
     * @return accessToken || null
     */
    public String resolveToken(HttpServletRequest request){
//        String token = request.getHeader(header);
//        if(StringUtils.hasText(token)){
//            return token;
//        }
//        return null;
            String token;
            try {
                token = request.getHeader(header);
            }catch (Exception e) {
                System.out.println(e.getMessage());
                token = null;
            }
        return token;
    }
    /**
     * 에러 처리를 위해 따로 만들어 놓음.
     * @param token accessToken
     * @return token 의 Claims 내용.
     */
    public Claims parseClaims(String token){
        try{
            return Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();
        }catch (ExpiredJwtException e){
            throw new CustomRuntimeException(ErrorCode.EXPIRED_TOKEN_EXCEPTION);
        }
    }

    /**
     * 토큰이 유효하지 않으면 예외 발생.
     * @param token jwt 토큰
     * @return 유효성 여부 || 예외
     */
    public boolean isValid(String token){
        try{
            Jwts.parser().verifyWith(key).build().parseSignedClaims(token) ;
            return true;
        } catch (UnsupportedJwtException e){
            throw new CustomRuntimeException(ErrorCode.UNSUPPORTED_JWT_EXCEPTION);
        } catch (ExpiredJwtException e){
            throw new CustomRuntimeException(ErrorCode.EXPIRED_TOKEN_EXCEPTION);
        } catch (MalformedJwtException e){
            throw new CustomRuntimeException(ErrorCode.MALFORMED_JWT_CLAIMS);
        } catch (JwtException | IllegalArgumentException e){
            throw new CustomRuntimeException(ErrorCode.ILLEGAL_JWT_EXCEPTION);
        }
    }

    /**
     * 토큰의 유효성 검증 진행 후 토큰에 존재하는 userId 반환
     * TODO : 상황에 따라서 에외 발생을 안시키거나 만기된 토큰을 재발급 시키거나 할 수 있으므로 수정이 필요하다.
     * @param token accessToken
     * @return userId
     */
    public Integer parseUserId(String token){
        if(!checking.checkString(token)){
            throw new CustomRuntimeException(ErrorCode.NEED_LOGIN_EXCEPTION);
        }
        if(!this.isValid(token)){
            throw new CustomRuntimeException(ErrorCode.EXPIRED_TOKEN_EXCEPTION);
        }
        String userId = this.getAuthentication(token).getName();
        if(!checking.checkString(userId)){
            throw new CustomRuntimeException(ErrorCode.ILLEGAL_JWT_EXCEPTION);
        }
        return (int) Float.parseFloat(userId);
    }

    /**
     * 정확하게는 모르겠으나, 여기에서 name 으로 userId 를 넣었다는 건 반드시 알고 있어야 함.
     * @param token accessToken
     * @return ?? 나도 몰라.
     */
    public Authentication getAuthentication(String token){
        Claims claims = parseClaims(token);
        List<SimpleGrantedAuthority> authority =
                new ArrayList<>(Arrays.asList(
                        claims.get("auth").toString().split(","))).stream().map(SimpleGrantedAuthority::new).toList()
                ;
        User user = new User(claims.get("id").toString(), "" ,authority);
        return new UsernamePasswordAuthenticationToken(user , "" , authority);
    }

}
