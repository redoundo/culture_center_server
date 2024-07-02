package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * category table entity
 */
@Data
@Entity
@Table(name = "categories")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Categories {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="categoryId", nullable = false, unique = true)
    private Integer categoryId;
    @Column(name = "categoryName", nullable = false)
    private String categoryName;
    @Column(name = "targetId", nullable = false)
    private Integer targetId;
}
