package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * applied table entity
 */
@Data
@Entity
@Table(name = "applied")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Applied {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="appliedId", nullable = false, unique = true)
    private Integer appliedId;
    @Column(name = "appliedLectureId", nullable = false)
    private Integer appliedLectureId;
    @Column(name = "appliedUserId", nullable = false)
    private Integer appliedUserId;
}
