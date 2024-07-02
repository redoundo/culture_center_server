package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.CreationTimestamp;

import java.sql.Timestamp;

/**
 * users table entity
 */
@Data
@Entity
@Table(name = "users")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Users {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="userId", nullable = false, unique = true)
    private Integer userId;
    @Column(name = "email", nullable = false, unique = true)
    private String email;
    @Column(name = "nickname", nullable = false, unique = true)
    private String nickname;
    @Column(name = "password", nullable = false)
    private String password;

    @Column(name = "registerDate")
    @CreationTimestamp
    private Timestamp registerDate;
    @Column(name = "snsProvider", nullable = false)
    private String snsProvider;
    @Column(name = "snsProviderId", nullable = false, unique = true)
    private String snsProviderId;
    @ColumnDefault("0")
    @Column(name = "wantFcmMessage")
    private Integer wantFcmMessage;
    @Column(name = "fcmToken", unique = true)
    private String fcmToken;
}
