import numpy as np
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkCubeSource, vtkSphereSource, vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderer, vtkRenderWindowInteractor, vtkWindowToImageFilter)


def init_visualize(argv, dims, body, filename):
    dt=1
    len_x=dims[0]
    len_y=dims[1]
    len_z = dims[2]
    n=len_x*len_y*len_z

    #скорости
    v1 = np.zeros([n], dtype=np.float64)
    v2 = np.zeros([n], dtype=np.float64)
    v3 = np.zeros([n], dtype=np.float64)

    for i in range(len_x):
        for j in range(len_y):
            for k in range(len_z):
                v1[dims[1]*dims[2]*i+dims[2]*j+k] = body.mp[i, j, k].V[0]
                v2[dims[1]*dims[2]*i+dims[2]*j+k] = body.mp[i, j, k].V[1]
                v3[dims[1]*dims[2]*i+dims[2]*j+k] = body.mp[i, j, k].V[2]
    conRadius = 0.05
    sphereRadius = 0.06
    color_sphere = (0.0, 0.0, 1.0)
    color_con = (1.0, 0.0, 0.0)
    color_background = (1, 1, 1)
    picture_size_x = 1200
    picture_size_y = 1200
    title = "Velocity"

    # создаём экземпляр vtkConeSource, эти экземпляры могут обрабатывать фильтры
    sphere = vtkSphereSource()
    sphere.SetRadius(sphereRadius)

    con=[0]*n
    for i in range(n):
        con[i] = vtkConeSource()
        con[i].SetRadius(conRadius)

    # создаем экземпляр vtkPolyDataMapper для отображения полигональных данных в графические примитивы
    sphereMapper = vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    conMapper=[0]*n
    for i in range(n):
        conMapper[i] = vtkPolyDataMapper()
        conMapper[i].SetInputConnection(con[i].GetOutputPort())

    #задаём некоторые общие свойства
    property1 = vtkProperty()
    property1.SetColor(color_sphere)
    property1.SetDiffuse(0.7)
    property1.SetSpecular(0.4)
    property1.SetSpecularPower(20)

    property2 = vtkProperty()
    property2.SetColor(color_con)
    property2.SetDiffuse(0.7)
    property2.SetSpecular(0.4)
    property2.SetSpecularPower(20)

    #создание моделей конусов и шаров
    sphereActor1 = [0] * n
    conActor = [0] * n
    for i in range(dims[0]):
        for j in range(dims[1]):
            for z in range(dims[2]):
                sphereActor1[dims[1]*dims[2]*i+dims[2]*j+z] = vtkActor()
                sphereActor1[dims[1]*dims[2]*i+dims[2]*j+z].SetMapper(sphereMapper)
                sphereActor1[dims[1]*dims[2]*i+dims[2]*j+z].SetProperty(property1)
                sphereActor1[dims[1]*dims[2]*i+dims[2]*j+z].SetPosition(i, j, z)

                if v1[dims[1]*dims[2]*i+dims[2]*j+z]**2 + v2[dims[1]*dims[2]*i+dims[2]*j+z]**2 + v3[dims[1]*dims[2]*i+dims[2]*j+z]**2 > 0:
                    con[dims[1] * dims[2] * i + dims[2] * j + z].SetHeight(1)
                else:
                    con[dims[1] * dims[2] * i + dims[2] * j + z].SetHeight(0)
                conActor[dims[1] * dims[2] * i + dims[2] * j + z] = vtkActor()
                conActor[dims[1] * dims[2] * i + dims[2] * j + z].SetMapper(conMapper[dims[1] * dims[2] * i + dims[2] * j + z])
                conActor[dims[1] * dims[2] * i + dims[2] * j + z].SetProperty(property2)
                conActor[dims[1] * dims[2] * i + dims[2] * j + z].SetPosition(i, j, z)

                con[dims[1]*dims[2]*i+dims[2]*j+z].SetDirection(v1[dims[1]*dims[2]*i+dims[2]*j+z], v2[dims[1]*dims[2]*i+dims[2]*j+z], v3[dims[1]*dims[2]*i+dims[2]*j+z])
                conMapper[dims[1]*dims[2]*i+dims[2]*j+z].SetInputConnection(con[dims[1]*dims[2]*i+dims[2]*j+z].GetOutputPort())

    ren1 = vtkRenderer()
    #добавление моделей на изображение
    for i in sphereActor1:
        if i != 0:
            ren1.AddActor(i)
    for i in conActor:
        if i != 0:
            ren1.AddActor(i)
    ren1.SetBackground(color_background)

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(picture_size_x, picture_size_y)
    renWin.SetWindowName(title)

    #подключение камеры
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    camera = ren1.GetActiveCamera()
    camera.SetViewUp(0, 0, 1)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetPosition(10, 10, 10)
    ren1.ResetCamera()
    camera.Dolly(1.0)
    ren1.ResetCameraClippingRange()

    renWin.Render()
    #iren.Start()

    # Перевод окна в картинку формата PNG
    windowto_image_filter = vtkWindowToImageFilter()
    windowto_image_filter.SetInput(renWin)
    windowto_image_filter.SetScale(1)  # image quality
    windowto_image_filter.SetInputBufferTypeToRGBA()
    windowto_image_filter.Update()

    writer = vtkPNGWriter()
    writer.SetInputConnection(windowto_image_filter.GetOutputPort())
    writer.SetFileName(filename)
    writer.Write()