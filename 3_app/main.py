from flask import Flask, request, render_template
import settings
import utils
import numpy as np
import cv2
import predictions as pred

app = Flask(__name__)
app.secret_key = 'document_scanner_app'

docscan = utils.DocumentScan()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def scandoc():
    if request.method == 'POST':
        file = request.files.get('image_name')

        if file is None or file.filename == '':
            return render_template(
                'scanner.html',
                fileupload=False,
                message='❌ No file selected.'
            )

        if not allowed_file(file.filename):
            return render_template(
                'scanner.html',
                fileupload=False,
                message='❌ Unsupported file type. Please upload PNG, JPG, or JPEG image.'
            )

        upload_image_path = utils.save_upload_image(file)
        print('Image saved in =', upload_image_path)

        four_points, size = docscan.document_scanner(upload_image_path)
        print(four_points, size)

        if four_points is None:
            points = [
                {'x': 10, 'y': 10},
                {'x': 120, 'y': 10},
                {'x': 120, 'y': 120},
                {'x': 10, 'y': 120}
            ]
            message = '⚠️ Unable to locate document corners. Default points loaded.'
        else:
            points = utils.array_to_json_format(four_points)
            message = '✅ Document corners detected successfully.'

        return render_template(
            'scanner.html',
            points=points,
            fileupload=True,
            message=message
        )

    return render_template('scanner.html', fileupload=False)


@app.route('/transform', methods=['POST'])
def transform():
    try:
        points = request.json.get('data')
        if points is None:
            return 'fail'

        array = np.array(points)
        magic_color = docscan.calibrate_to_original_size(array)

        filename = 'magic_color.jpg'
        magic_image_path = settings.join_path(settings.MEDIA_DIR, filename)
        cv2.imwrite(magic_image_path, magic_color)

        return 'success'
    except Exception as e:
        print('Transform Error:', e)
        return 'fail'


@app.route('/prediction')
def prediction():
    try:
        wrap_image_filepath = settings.join_path(settings.MEDIA_DIR, 'magic_color.jpg')
        image = cv2.imread(wrap_image_filepath)

        if image is None:
            return render_template(
                'predictions.html',
                results=[],
                message='❌ Processed image not found.'
            )

        image_bb, results = pred.getPredictions(image)

        bb_filename = settings.join_path(settings.MEDIA_DIR, 'bounding_box.jpg')
        cv2.imwrite(bb_filename, image_bb)

        return render_template('predictions.html', results=results)

    except Exception as e:
        print('Prediction Error:', e)
        return render_template(
            'predictions.html',
            results=[],
            message='❌ Error while generating predictions.'
        )


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)