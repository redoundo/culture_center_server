package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * centers table entity
 */
@Data
@Entity
@Table(name = "centers")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Centers {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "centerId", unique = true, nullable = false)
    private Integer centerId;
    @Column(name="centerName", nullable = false)
    private String centerName;
    @Column(name="centerRealName", nullable = false, unique = true)
    private String centerRealName;
    @Column(name="centerType", nullable = false)
    private String centerType;
    @Column(name="centerUrl", nullable = false)
    private String centerUrl;
}
