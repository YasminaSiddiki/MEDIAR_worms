import argparse

import torch
from train_tools.models import MEDIARFormer
from core.MEDIAR import Predictor, EnsemblePredictor


def predict(
        input_path: str,
        output_path: str,
        prediction_mode: str = "ensemble",
        weights1_path: str = "MEDIAR_worms/models/model1.pth",
        weights2_path: str = "MEDIAR_worms/models/model2.pth"
):
    """
    Conducts prediction using either a single model or an ensemble of models, based on the specified prediction mode.

    The function initializes two models (model1 and model2) of type MEDIARFormer with specified model arguments.
    It then loads their weights from given paths (weights1_path and weights2_path). Depending on the prediction_mode,
    it uses either model1, model2, or an ensemble of both for prediction. The prediction results are saved to the
    output_path. Prediction is performed on the data located at input_path.

    Args:
    - input_path (str): The path to the input data file(s) to be processed.
    - output_path (str): The path where the prediction results should be saved.
    - prediction_mode (str, optional): Determines the prediction mode.
      Possible values are "model1", "model2", or "ensemble".
      Defaults to "ensemble".
    - weights1_path (str, optional): The file path to the weights for model1.
    - weights2_path (str, optional): The file path to the weights for model2.

    Returns:
    None: The function does not return a value but outputs the prediction results directly to the specified output path.
    """
    # Model initialization and configuration
    model_args = {
        "classes": 1,
        "decoder_channels": [1024, 512, 256, 128, 64],
        "decoder_pab_channels": 256,
        "encoder_name": 'mit_b5',
        "in_channels": 3
    }

    # Load model1 with weights if specified
    weights1 = torch.load(weights1_path, map_location="cpu") if weights1_path else None
    model1 = MEDIARFormer(**model_args)
    model1.load_state_dict(weights1, strict=False) if weights1 else None

    # Load model2 with weights if specified
    weights2 = torch.load(weights2_path, map_location="cpu") if weights2_path else None
    model2 = MEDIARFormer(**model_args)
    model2.load_state_dict(weights2, strict=False) if weights2 else None

    # Prediction process based on the mode
    if prediction_mode == "model1":
        # Predict using only model1
        predictor = Predictor(model1, "cuda:0", input_path, output_path, algo_params={"use_tta": False})
        _ = predictor.conduct_prediction()
    elif prediction_mode == "model2":
        # Predict using only model2
        predictor = Predictor(model2, "cuda:0", input_path, output_path, algo_params={"use_tta": False})
        _ = predictor.conduct_prediction()
    elif prediction_mode == "ensemble":
        # Predict using an ensemble of model1 and model2
        predictor = EnsemblePredictor(model1, model2, "cuda:0", input_path, output_path, algo_params={"use_tta": False})
        _ = predictor.conduct_prediction()


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Predict the output using single or ensemble models.")

    # Adding the arguments
    parser.add_argument('--input_path', type=str, required=True,
                        help='Path to the input data file(s).')
    parser.add_argument('--output_path', type=str, required=True,
                        help='Path where the prediction results will be saved.')
    parser.add_argument('--prediction_mode', type=str, default="ensemble",
                        choices=["model1", "model2", "ensemble"],
                        help='Prediction mode: "model1", "model2", or "ensemble". Defaults to "ensemble".')
    parser.add_argument('--weights1_path', type=str, default="MEDIAR_worms/models/model1.pth",
                        help='File path to the weights for model1.')
    parser.add_argument('--weights2_path', type=str, default="MEDIAR_worms/models/model2.pth",
                        help='File path to the weights for model2.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the predict function with the parsed arguments
    predict(
        input_path=args.input_path,
        output_path=args.output_path,
        prediction_mode=args.prediction_mode,
        weights1_path=args.weights1_path,
        weights2_path=args.weights2_path
    )


if __name__ == "__main__":
    main()
