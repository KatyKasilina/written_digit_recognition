
### TRAIN CNN MODEL
def fit(model, train_loader):
    optimizer = torch.optim.Adam(model.parameters())#,lr=0.001, betas=(0.9,0.999))
    error = nn.CrossEntropyLoss()
    EPOCHS = 5
    model.train()
    for epoch in range(EPOCHS):
        correct = 0
        for batch_idx, (X_batch, y_batch) in enumerate(train_loader):
            var_X_batch = Variable(X_batch).float()
            var_y_batch = Variable(y_batch)
            optimizer.zero_grad()
            output = model(var_X_batch)
            loss = error(output, var_y_batch)
            loss.backward()
            optimizer.step()

            # Total correct predictions
            predicted = torch.max(output.data, 1)[1]
            correct += (predicted == var_y_batch).sum()
            #print(correct)
            if batch_idx % 50 == 0:
                print('Epoch : {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\t Accuracy:{:.3f}%'.format(
                    epoch, batch_idx*len(X_batch), len(train_loader.dataset), 100.*batch_idx / len(train_loader), loss.item(), float(correct*100) / float(BATCH_SIZE*(batch_idx+1))))


def evaluate(model):
    correct = 0
    for test_imgs, test_labels in test_loader:
        test_imgs = Variable(test_imgs).float()
        output = model(test_imgs)
        predicted = torch.max(output,1)[1]
        correct += (predicted == test_labels).sum()
    print("Test accuracy:{:.3f}% ".format( float(correct) / (len(test_loader)*BATCH_SIZE)))



cnn = cnn_pytorch.CNN()

df = pd.read_csv('models/train.csv')
BATCH_SIZE = 32

y = df['label'].values
X = df.drop(['label'],1).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

torch_X_train = torch.from_numpy(X_train).type(torch.LongTensor)
torch_y_train = torch.from_numpy(y_train).type(torch.LongTensor) # data type is long

# create feature and targets tensor for test set.
torch_X_test = torch.from_numpy(X_test).type(torch.LongTensor)
torch_y_test = torch.from_numpy(y_test).type(torch.LongTensor)
##torch_y_test = torch.from_numpy(y_test).type(torch.LongTensor) # data type is long

##v-
torch_X_train = torch_X_train.view(-1, 1, 28, 28).float()/255.0
torch_X_test = torch_X_test.view(-1, 1, 28, 28).float()/255.0

print(torch_X_train.shape)
print(torch_X_test.shape)

# Pytorch train and test sets
train = torch.utils.data.TensorDataset(torch_X_train,torch_y_train)
test = torch.utils.data.TensorDataset(torch_X_test,torch_y_test)

# data loader
train_loader = torch.utils.data.DataLoader(train, batch_size = BATCH_SIZE, shuffle = False)
test_loader = torch.utils.data.DataLoader(test, batch_size = BATCH_SIZE, shuffle = False)

fit(cnn, train_loader)

evaluate(cnn)


torch.save(cnn.state_dict(), 'models/cnn_mnist.pt')

#################
## confusion matrix

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
torch_X_test = torch.from_numpy(x_test).type(torch.LongTensor)
#torch_y_test = torch.from_numpy(y_train).type(torch.LongTensor)
torch_X_test = torch_X_test.view(-1, 1, 28, 28).float()/255.0

_, predicted = torch.max(cnn(torch_X_test), 1)

test_labels = predicted.detach().numpy()
cm = confusion_matrix(test_labels, y_test)
df_cm = pd.DataFrame(cm)

plt.figure(figsize=(5, 5))
sns.heatmap(df_cm,  annot=True, cmap='Blues', fmt='g', cbar=False)
plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
plt.title('Confusion matrix PyTorch CNN', fontweight="bold", fontsize=15)


cm.diagonal()/cm.sum(axis=0)