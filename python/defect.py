import os
import sys
import shutil
import uuid
import mimetypes
import json
from ultralytics import YOLO


def main(file_path):
    model_dir = 'sources/models/best.pt'
    output_dir = ''

    mime_type, _ = mimetypes.guess_type(file_path)
    unique_id = uuid.uuid4().hex
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    type_name = os.path.splitext(os.path.basename(file_path))[1]

    if mime_type and mime_type.startswith('image'):
        output_dir = 'sources/res_imgs'
    elif mime_type and mime_type.startswith('video'):
        output_dir = 'sources/res_vid'

    model = YOLO(model_dir)
    results = model(file_path, show=False, conf=0.3, save=True, verbose=False)

    unique_file_path = os.path.join(output_dir, f"{base_name}_{unique_id}{type_name}")
    temp_file_path = os.path.join('../public/runs/detect/predict', base_name + type_name)
    os.rename(temp_file_path, unique_file_path)
    shutil.rmtree('runs')

    defect_classes = []
    for result in results:
        [defect_classes.append(model.names[int(obj.cls)]) for obj in result.boxes if
         model.names[int(obj.cls)] not in defect_classes]

    json_data = {
        'image': unique_file_path,
        'results': defect_classes  # Это может быть любой объект или структура данных, которые вы хотите вернуть
    }

    print(json.dumps(json_data))

if __name__ == '__main__':
    file_path = sys.argv[1]
    main(file_path)
