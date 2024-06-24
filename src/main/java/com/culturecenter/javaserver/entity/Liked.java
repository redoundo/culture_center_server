package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * liked table entity
 */
@Data
@Entity
@Table(name = "liked")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Liked {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="likedId", nullable = false, unique = true)
    private Integer likedId;
    @Column(name = "likedLectureId", nullable = false)
    private Integer likedLectureId;
    @Column(name = "likedUserId", nullable = false)
    private Integer likedUserId;
}
