# Code source: Gaël Varoquaux
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

from relocation.management import load

import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV

def scale_center(in_array):
	mean = in_array.mean(axis=0)  # make it give the mean calculated by each column
	std = in_array.std(axis=0)  # std deviation by column
	result = (in_array - mean)/std

	return result

def nick_test():
	logistic = linear_model.LogisticRegression()

	pca = decomposition.PCA()
	pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])

	data = load.get_relocation_information_as_ndarray()
	X_data = data[:,:-1]  # load in all the data for now, but strip off the targets
	Y_data = data[:,-1]   # load in all the targets
	###############################################################################
	# Plot the PCA spectrum
	pca.fit(X_data)

	plt.figure(1, figsize=(4, 3))
	plt.clf()
	plt.axes([.2, .2, .7, .7])
	plt.plot(pca.explained_variance_, linewidth=2)
	plt.axis('tight')
	plt.xlabel('n_components')
	plt.ylabel('explained_variance_')

	###############################################################################
	# Prediction

	n_components = 11
	Cs = np.logspace(-4, 4, 3)

	# Parameters of pipelines can be set using ‘__’ separated parameter names:

	estimator = GridSearchCV(pipe,
							 dict(logistic__C=Cs))
	estimator.fit(X_data, Y_data)

	#plt.axvline(estimator.best_estimator_.named_steps['pca'].n_components,
	#			linestyle=':', label='n_components chosen')
	plt.legend(prop=dict(size=12))
	plt.show()

def test():
	logistic = linear_model.LogisticRegression()

	pca = decomposition.PCA()
	pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])

	digits = datasets.load_digits()
	X_digits = digits.data
	y_digits = digits.target

	###############################################################################
	# Plot the PCA spectrum
	pca.fit(X_digits)

	plt.figure(1, figsize=(4, 3))
	plt.clf()
	plt.axes([.2, .2, .7, .7])
	plt.plot(pca.explained_variance_, linewidth=2)
	plt.axis('tight')
	plt.xlabel('n_components')
	plt.ylabel('explained_variance_')

	###############################################################################
	# Prediction

	n_components = [20, 40, 64]
	Cs = np.logspace(-4, 4, 3)

	#Parameters of pipelines can be set using ‘__’ separated parameter names:

	estimator = GridSearchCV(pipe,
							 dict(pca__n_components=n_components,
								  logistic__C=Cs))
	estimator.fit(X_digits, y_digits)

	plt.axvline(estimator.best_estimator_.named_steps['pca'].n_components,
				linestyle=':', label='n_components chosen')
	plt.legend(prop=dict(size=12))
	plt.show()
