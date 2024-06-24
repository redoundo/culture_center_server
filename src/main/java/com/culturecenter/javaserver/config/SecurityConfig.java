package com.culturecenter.javaserver.config;
import com.culturecenter.javaserver.auth.JwtAuthDeniedHandler;
import com.culturecenter.javaserver.auth.JwtAuthEntryPoint;
import com.culturecenter.javaserver.auth.JwtProvider;
import com.culturecenter.javaserver.filter.JwtFilter;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.context.SecurityContextRepository;

/**
 * spring security configuration
 */
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthEntryPoint entryPoint;
    private final JwtAuthDeniedHandler deniedHandler;
    private final JwtProvider jwtProvider;
    private final SecurityContextRepository repository = new HttpSessionSecurityContextRepository();
    @Bean
    public BCryptPasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain jwtChain(HttpSecurity security) throws Exception {
        security.securityMatcher("/api/auth/**", "/api/user/**", "/api/lecture/**")
                .csrf(AbstractHttpConfigurer::disable)
                .exceptionHandling((exception)->
                        exception
                                .authenticationEntryPoint(entryPoint)
                                .accessDeniedHandler(deniedHandler)
                )
                .authorizeHttpRequests((authorizeHttpRequests) -> {
                    authorizeHttpRequests
                            .requestMatchers("/api/auth/**", "/api/user/auth/isValid" ).permitAll()
                            .requestMatchers( "/api/lecture/**").permitAll();
                    authorizeHttpRequests.requestMatchers("/api/user/**").hasRole("USER");
                })
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .addFilterBefore(new JwtFilter(jwtProvider, repository), UsernamePasswordAuthenticationFilter.class);
        return security.build();
    }

    @Bean
    public WebSecurityCustomizer ignoreUrl() throws Exception {
        return (web) -> web.ignoring()
                .requestMatchers( "/js/**", "/css/**");
    }
}
