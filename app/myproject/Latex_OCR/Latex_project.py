# Latex公式识别测试
import os
from PIL import Image
from pix2tex.cli import LatexOCR


if __name__ == '__main__':
    for i in range(50):
        print("请输入您要检测的公式图片名字：")
        x = input()
        # 如果输入的是quit，则退出程序
        if x =='quit':
            print("Press any key to continue...")
            os.system('pause')
        else:
            image = 'input/{}.png'.format(x)
            img = Image.open(image)
            model = LatexOCR()
            print(f"{image.split('/')[-1]}的LaTeX公式识别为：{model(img)}\n")
    print("Press any key to continue...")
    os.system('pause')

class LatexOCR():
    # 传入图片
    def __init__(self, image):
        self.image = image
        self.model = LatexOCR()

    def ToLatex(self):
        return self.model(self.image)
    # # 加载模型
    # def load_model(self):
    #     model = Model()
    #     model.load_state_dict(torch.load('model/weights.pth', map_location='cpu'))
    #     model.eval()
    #     return model