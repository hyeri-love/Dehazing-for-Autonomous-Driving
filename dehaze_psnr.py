import cv2
from skimage.metrics import structural_similarity as ssim

# 使用示例
if __name__ == "__main__":
    try:
        # 读取雾天图像和参考无雾图像
        dehazed_img = cv2.imread("dehazed_image.jpg")
        reference_img = cv2.imread("reference.jpg")

        if dehazed_img is None or reference_img is None:
            raise ValueError("One of the images could not be loaded. Check the file paths.")

        if dehazed_img.shape != reference_img.shape:
            raise ValueError("Image dimensions do not match.")
        # 确保图像为灰度图或转换为灰度图
        dehazedimg_gray = cv2.cvtColor(dehazed_img, cv2.COLOR_BGR2GRAY)
        referenceimg_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)

        # 计算并打印PSNR
        psnr_value = cv2.PSNR(reference_img, dehazed_img)
        print(f"PSNR: {psnr_value} dB")
        # 计算并打印SSIM
        ssim_value, _ = ssim(referenceimg_gray, dehazedimg_gray, full=True)
        print(f"SSIM: {ssim_value}")

    except Exception as e:

        print(f"An error occurred: {e}")
