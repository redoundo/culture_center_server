package com.culturecenter.javaserver.auth;

import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * 접근을 위한 권한이 없을 때
 */
@Component
@RequiredArgsConstructor
public class JwtAuthDeniedHandler implements AccessDeniedHandler {
    private final JwtProvider jwtProvider;

    @Override
    public void handle(HttpServletRequest request,
                       HttpServletResponse response,
                       AccessDeniedException accessDeniedException) throws IOException, ServletException {
        String token = this.jwtProvider.resolveToken(request);
        if (token != null && this.jwtProvider.isValid(token)) throw new CustomRuntimeException(ErrorCode.JWT_IS_VALID_BUT_SOMETHING_GOT_WRONG);
        else response.sendError(HttpServletResponse.SC_FORBIDDEN);
    }
}
