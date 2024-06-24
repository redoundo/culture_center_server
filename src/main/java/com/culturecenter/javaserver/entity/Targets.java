package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * target table
 */
@Data
@Entity
@Table(name = "targets")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Targets {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "targetId", unique = true, nullable = false)
    private Integer targetId;
    @Column(name="targetName", nullable = false)
    private String targetName;
}
