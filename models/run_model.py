import pandas as pd

from seqtoseq import *
from create_dataset import preprocess
from train import trainIters
from predict import evaluateRandomly
import torch
import pickle
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
epochs= 5
print_evy = 1
model_path = "model_large"
# reload = f"{model_path}_v5"
reload = None
# print(reload)

transformed_dataset = preprocess(train_manifest_path='/home/ubuntu/commonvoice_validated_manifest.json', cloud=True)

encoder1 = EncoderRNN(mels_dims*MAX_LENGTH, 256).to(device)

# encoder1 = EncoderRNN(mels_dims, 256).to(device)
decoder1 = AttnDecoderRNN(256, 29, dropout_p=0.1).to(device)



# encoder1 = Encoder(80, 512, 2, dropout=0.1, bidirectional=True).to(device)
# decoder1 = Decoder(vocab_size=29, embedding_dim=100, hidden_size=1024, num_layers=4).to(device)



trainIters(transformed_dataset,encoder1, decoder1, n_iters=epochs,model_save_path=model_path, print_every=print_evy,
                        learning_rate=0.001,reload_path=reload)
evaluateRandomly(transformed_dataset,encoder1, decoder1,10)




# with open('output/encoder_vars_simple.pkl', 'wb') as convert_file:
#     pickle.dump(encoder1,convert_file)

# with open('output/decoder_vars_simple.pkl', 'wb') as convert_file:
#     pickle.dump(decoder1,convert_file)


enc_path = f"output/enc_{model_path}"
torch.save(encoder1.state_dict(), enc_path)
dec_path = f"output/dec_{model_path}"
torch.save(decoder1.state_dict(), dec_path)







