
import cv2
import numpy as np

class Dehazer:
    def __init__(self, patch_size=15, omega=0.95, t0=0.1):
        self.patch_size = patch_size
        self.omega = omega  # 雾浓度系数 (0~1)
        self.t0 = t0  # 最小透射率阈值

    def _dark_channel(self, img):
        """计算暗通道"""
        min_channel = np.min(img, axis=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.patch_size, self.patch_size))
        return cv2.erode(min_channel, kernel)

    def _estimate_atmospheric_light(self, img, dark):
        """估计大气光值"""
        flat_img = img.reshape(-1, 3)
        flat_dark = dark.flatten()

        # 选择暗通道最亮的0.1%像素
        num_pixels = flat_dark.shape[0]
        top_indices = np.argpartition(flat_dark, -int(num_pixels * 0.001))[-int(num_pixels * 0.001):]

        # 取这些像素中亮度最高的作为大气光
        atmospheric_light = np.max(flat_img[top_indices], axis=0)
        return atmospheric_light

    def dehaze(self, img):
        """主去雾函数"""
        img = img.astype(np.float32) / 255.0
        dark = self._dark_channel(img)

        atmospheric_light = self._estimate_atmospheric_light(img, dark)
        normalized_img = img / atmospheric_light

        transmission = 1 - self.omega * self._dark_channel(normalized_img)
        transmission = np.clip(transmission, self.t0, 1.0)

        # 恢复无雾图像
        result = np.zeros_like(img)
        for i in range(3):
            result[..., i] = (img[..., i] - atmospheric_light[i]) / transmission + atmospheric_light[i]

        return np.clip(result * 255, 0, 255).astype(np.uint8)


# 使用示例
if __name__ == "__main__":
    # 读取图像（替换为您的CARLA雾天图像路径）
    hazy_img = cv2.imread("carla_foggy.jpg")

    if hazy_img is None:
        print("错误：无法加载图像，请检查路径")
    else:
        dehazer = Dehazer(patch_size=15, omega=0.95)
        dehazed_img = dehazer.dehaze(hazy_img)

        # 显示对比结果
        cv2.imshow("Original", hazy_img)
        cv2.imshow("Dehazed", dehazed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 保存结果
        cv2.imwrite("dehazed_result.jpg", dehazed_img)