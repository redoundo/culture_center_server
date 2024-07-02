package com.culturecenter.javaserver.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * branch table entity
 */
@Data
@Entity
@Table(name = "branches")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Branches {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="branchId", nullable = false, unique = true)
    private Integer branchId;
    @Column(name = "branchName", nullable = false)
    private String branchName;
    @Column(name = "branchAddress", nullable = false)
    private String branchAddress;
    @Column(name = "centerOfBranch", nullable = false)
    private Integer centerOfBranch;
    @Column(name="latitude", nullable = false)
    private Double latitude;
    @Column(name="longitude", nullable = false)
    private Double longitude;

}
