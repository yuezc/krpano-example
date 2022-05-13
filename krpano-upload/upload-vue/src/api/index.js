import { request } from "./request";

// 提交图片API
export const submitIMG = (e) => {
    return request({
        url: "/upload_image",
        method: "post",
        data: e,
        headers: {
            "Content-Type": "multipart/form-data"
        },
    })
}

// 图片上传完成，创建全景API
export const createVR = () => {
    return request({
        url: "/create",
        method: "post"
    })
}

