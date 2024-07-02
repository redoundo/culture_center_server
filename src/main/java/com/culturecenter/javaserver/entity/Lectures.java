package com.culturecenter.javaserver.entity;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.Type;
import org.springframework.lang.Nullable;

import java.sql.Timestamp;
import java.util.Map;

/**
 * lectures table entity
 */
@Data
@Entity
@Table(name = "lectures")
@Getter
@Setter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Lectures {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "lectureId", unique = true, nullable = false)
    private Integer lectureId;
    @Column(name="center", nullable = false)
    private String center;
    @Column(name="type", nullable = false)
    private String type;
    @Column(name="region", nullable = false)
    private String region;
    @Column(name="branch", nullable = false)
    private String branch;
    @Column(name="address", nullable = false)
    private String address;
    @Column(name="target", nullable = false)
    private String target;
    @Column(name="category", nullable = false)
    private String category;
    @Column(name="title", nullable = false)
    private String title;
    @Column(name="url", nullable = false, unique = true)
    private String url;
    @Column(name="src", nullable = false)
    private String src;
    @Column(name="price", nullable = false)
    private Integer price;
    @Column(name="content", nullable = false)
    private String content;
    @Column(name="adult", nullable = false)
    private String adult;
    @Column(name="kid", nullable = false)
    private String kid;
    @Column(name="baby", nullable = false)
    private String baby;
    @Column(name="lectureStart", nullable = false)
    private Timestamp lectureStart;
    @Column(name="lectureEnd", nullable = false)
    private Timestamp lectureEnd;
    @Column(name="enrollStart")
    private Timestamp enrollStart;
    @Column(name="enrollEnd")
    private Timestamp enrollEnd;
    @Column(name="lectureSupplies")
    private String lectureSupplies;

    @Column(name="curriculum")
    @Type(JsonType.class)
    private Map<String, Object> curriculum;
    @Column(name="crawledDate", nullable = false)
    private Timestamp crawledDate;
    @Column(name="lectureHeldDates")
    private String lectureHeldDates;
    @Column(name="enrollStatus")
    private String enrollStatus;
}
