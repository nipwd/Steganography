import binascii
from PIL import Image

class LSBSteg:
    def __init__(self, im):
        self.image = im
        self.width, self.height = im.size
        self.mode = im.mode

    def hide(self, message):
        # Agrega caracteres de inicio y fin al mensaje
        message = "<start>" + message + "<end>"
        binary_message = ''.join(format(ord(i), '08b') for i in message)
        if len(binary_message) > self.width*self.height*3:
            raise ValueError("Message too large to fit in image")
        encoded = self.image.copy()
        self.put_binary(encoded, binary_message)
        self.image = encoded

    def show(self):
        binary_message = self.get_binary()
        n = int(binary_message, 2)
        message = binascii.unhexlify('%x' % n).decode('latin1')
        start_index = message.find("<start>")
        end_index = message.find("<end>")
        if start_index != -1 and end_index != -1:
            message = message[start_index+len("<start>"):end_index]
            print("El mensaje oculto es:", message)
        else:
            print("No se encontró ningún mensaje oculto en la imagen")
            main()

    def save(self, file_path):
        self.image.save(file_path)

    def put_binary(self, im, data):
        binary = list(data)
        pixels = im.load()
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                pixel = list(pixels[i, j])
                for n in range(3):
                    if len(binary) == 0:
                        pixels[i, j] = tuple(pixel)
                        return
                    val = pixel[n]
                    if val % 2 == 1:
                        pixel[n] -= 1
                    pixel[n] = pixel[n] | int(binary.pop(0))
                pixels[i, j] = tuple(pixel)

    def get_binary(self):
        binary = ""
        pixels = self.image.load()
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                pixel = list(pixels[i, j])
                for n in range(3):
                    binary += str(pixel[n] & 1)
        return binary

def main():
    # Opcion para guardar mensaje en imagen
    choice = input("---Desea ocultar un mensaje en una imagen (1) ---leer un mensaje oculto en una imagen (2)? ---Salir (3)")
    if choice == '1':
        try:
            # Selecciona la imagen y el mensaje a ocultar
            image_file = input("Introduce el nombre de la imagen: ")
            image = Image.open(image_file)
            message = input("Introduce el mensaje que deseas ocultar: ")
            # Oculta el mensaje en la imagen
            steg = LSBSteg(image)
            steg.hide(message)
            # Guarda la imagen con el mensaje oculto
            output_file = input("Introduce el nombre del archivo de salida: ")
            steg.save(output_file)
            print("Se ha guardado la imagen con el mensaje oculto.")
            main()
        except FileNotFoundError:
            print("{-} ERROR: Seleccionar archivo correcto")
            main()
    if choice == '2':
        try:
            # Selecciona la imagen y lee el mensaje oculto
            image_file = input("Introduce el nombre de la imagen: ")
            image = Image.open(image_file)
            steg = LSBSteg(image)
            steg.show()
        except FileNotFoundError:
            print("{-} ERROR: Seleccionar archivo correcto")
            main()
    if choice == '3':
        print("exit")
        quit()
    else:
        print("Opción no válida")
        main()
if __name__ == 'main':
	main()
main()