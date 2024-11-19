package com.example.moweb2;

import com.google.gson.annotations.SerializedName;

public class Post {

    @SerializedName("id")
    private int id;

    @SerializedName("title")
    private String title;

    @SerializedName("text")
    private String text;

    @SerializedName("created_date")
    private String createdDate;

    @SerializedName("image")
    private String image;

    // Getter 메서드들
    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getText() {
        return text;
    }

    public String getCreatedDate() {
        return createdDate;
    }

    public String getImage() {
        return image;
    }
}
