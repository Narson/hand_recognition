from math import sqrt, pow
import numpy
import cv2 as opencv

#klasa zbierajaca cala logike przetwarzania obrazu i obliczania charakterystyki dloni
class HandRecognition(object):
    def __init__(self, base_path, hand_files, result_file):
        self.hand_files = hand_files
        self.result_file = result_file
        self.base_path = base_path

    #wykonywanie obliczen koncowych
    def do_calculations(self):
        contours = []
        points = []
        lenghts = []
        ratio = []
        with open(result_file, "w") as res_file:
            for i in range(0,len(hand_files)):
                path = self.base_path + hand_files[i]
                picture = opencv.imread(path)
                contours.append(self.detect_contour(picture))
                points.append(self.detect_extreme_points(contours[i]))
                lenghts.append(self.count_lenghts(points[i]))
                if i > 0:
                    ratio.append(self.compare_lenghts(lenghts[0], lenghts[i]))
                print(hand_files[i], ' ', '%s\n' % lenghts[i])
            
            #plk_wyn.write('Podobienstwo pliku %s\n' % pliki_dloni[0])
            for i in range(0, len(ratio)):
                res_file.write('File %s is similar to %s in %s%%\n' % (hand_files[0], hand_files[i+1], ratio[i]))

            picture1 = opencv.imread(self.base_path + hand_files[0])
            self.draw_contour(contours[0], picture1)
            self.draw_lines(picture1, points)

            opencv.imshow("Picture with contour", picture1)


    #wykrywanie konturu dloni
    def detect_contour(self, picture):
        ycrcb_picture = opencv.cvtColor(picture, opencv.COLOR_BGR2YCR_CB)
        ycrcb_min_skin = numpy.array((0, 145, 80)) #wartosci sprawdzone w internecie i skorygowane, aby pasowaly do wykonanych zdjec
        ycrcb_max_skin = numpy.array((255, 170, 130)) #jak wyzej^
        ycrcb_skin = opencv.inRange(ycrcb_picture, ycrcb_min_skin, ycrcb_max_skin)
        _, contours, _ = opencv.findContours(ycrcb_skin, opencv.RETR_EXTERNAL, opencv.CHAIN_APPROX_SIMPLE)
        
        return contours

    #rysowanie konturu na zdjeciu
    def draw_contour(self, contours, picture):
        for i, c in enumerate(contours):
            area = opencv.contourArea(c)
            if area > 1000:
                opencv.drawContours(picture, contours, i, (255, 0, 0), 5)

    #rysowanie linii laczacych punkty skrajne
    def draw_lines(self, picture, points):
        for i in range(1, len(points[0])):
            opencv.line(picture, tuple(points[0][i - 1]), tuple(points[0][i]), (0, 0, 255), 4)
                
         
    #wykrywanie punktow skrajnych na rece
    def detect_extreme_points(self, contours):     
        points = []
        direction = {'where': 'up'}

        def count_contour(contour, direction):
            for i, point in enumerate(contour):
                x,y = point
                if i < len(contour) - 3:
                    x1, y1 = contour[i + 1]
                    x2, y2 = contour[i + 2]
                    if y > max(y1, y2) and direction['where'] == 'up':
                        points.append([x,y])
                        direction['where'] = 'down'
                    elif y < min(y1, y2) and direction['where'] == 'down':
                        points.append([x,y])
                        direction['where'] = 'up'
        
        [count_contour(contour.reshape(-1, 2), direction) for contour in contours]
                        
        return points

                    
    #obliczanie proporcji
    def count_lenghts(self, points):
        lenghts = []
        for value, next_value in zip(points, points[1:]+[points[0]]):
            lenghts.append(sqrt(pow(next_value[0]-value[0], 2) + pow(next_value[1]-value[1], 2)))
            
        return lenghts

                
    #porownanie konturow
    def compare_lenghts(self, lenghts1, lenghts2):
        ratio = 1;
        for i in range(0, 8):
            if lenghts1[i] >= lenghts2[i]:
                ratio += lenghts2[i] / lenghts1[i]
            else:
                ratio += lenghts1[i] / lenghts2[i]
                
        return int(ratio * 100 / 9)


#main
if __name__ == "__main__":
    hand_files = ['adam1.png', 'adam2.png', 'adam3.png', 'pawel1.png', 'pawel2.png', 'pawel3.png',
                   'maciej1.png', 'maciej2.png', 'norbi1.png', 'norbi2.png', 'norbi3.png', 'oli1.png', 'oli2.png', 'oli3.png'] 

    result_file = "D:\\PythonProjects\\hand_recognition\\results.txt"
    base_path = "D:\\PythonProjects\\hand_recognition\\hands"
    
    recognizer = HandRecognition(base_path, hand_files, result_file)

    recognizer.do_calculations()
    
    opencv.waitKey(0)
    opencv.destroyAllWindows()
