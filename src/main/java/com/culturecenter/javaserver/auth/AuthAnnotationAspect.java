package com.culturecenter.javaserver.auth;

import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import static com.culturecenter.javaserver.utils.Util.checking;


@Aspect
@Component
public class AuthAnnotationAspect {

    @Around("execution(* com.culturecenter.javaserver.controller.UserController..*(.., @com.culturecenter.javaserver.auth.AuthAnnotation (*), ..))")
    public Object userIdInAuthentication(ProceedingJoinPoint joinPoint) throws Throwable {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null) throw new CustomRuntimeException(ErrorCode.NEED_LOGIN_EXCEPTION);

        UserDetails userDetails = (UserDetails) auth.getPrincipal();
        if (userDetails == null || !checking.checkString(userDetails.getUsername()))
            throw new CustomRuntimeException(ErrorCode.FAILED_AUTHORIZED_EXCEPTION);

        Integer userId = (int) Float.parseFloat(userDetails.getUsername());
        Object[] objects = joinPoint.getArgs();
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        for (int i = 0; i < methodSignature.getMethod().getParameterCount(); i++) {
            if (methodSignature.getMethod().getParameters()[i].isAnnotationPresent(AuthAnnotation.class)) {
                objects[i] = userId;
            }
        }
        return joinPoint.proceed(objects);
    }

}
