# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Users\minorua\.qgis2\python\developing_plugins\Qgis2threejs\ui\vectorproperties.ui'
#
# Created: Fri May 29 10:15:44 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_VectorPropertiesWidget(object):
    def setupUi(self, VectorPropertiesWidget):
        VectorPropertiesWidget.setObjectName(_fromUtf8("VectorPropertiesWidget"))
        VectorPropertiesWidget.resize(346, 375)
        self.verticalLayout_2 = QtGui.QVBoxLayout(VectorPropertiesWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setContentsMargins(8, -1, 6, -1)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_ObjectType = QtGui.QLabel(VectorPropertiesWidget)
        self.label_ObjectType.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ObjectType.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_ObjectType.setObjectName(_fromUtf8("label_ObjectType"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_ObjectType)
        self.comboBox_ObjectType = QtGui.QComboBox(VectorPropertiesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_ObjectType.sizePolicy().hasHeightForWidth())
        self.comboBox_ObjectType.setSizePolicy(sizePolicy)
        self.comboBox_ObjectType.setObjectName(_fromUtf8("comboBox_ObjectType"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_ObjectType)
        self.verticalLayout_2.addLayout(self.formLayout_4)
        self.label_ObjectTypeMessage = QtGui.QLabel(VectorPropertiesWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_ObjectTypeMessage.setFont(font)
        self.label_ObjectTypeMessage.setStyleSheet(_fromUtf8("font-weight: bold;"))
        self.label_ObjectTypeMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ObjectTypeMessage.setWordWrap(True)
        self.label_ObjectTypeMessage.setObjectName(_fromUtf8("label_ObjectTypeMessage"))
        self.verticalLayout_2.addWidget(self.label_ObjectTypeMessage)
        self.groupBox_zCoordinate = QtGui.QGroupBox(VectorPropertiesWidget)
        self.groupBox_zCoordinate.setObjectName(_fromUtf8("groupBox_zCoordinate"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_zCoordinate)
        self.gridLayout_9.setContentsMargins(9, 3, 9, 3)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.verticalLayout_zCoordinate = QtGui.QVBoxLayout()
        self.verticalLayout_zCoordinate.setObjectName(_fromUtf8("verticalLayout_zCoordinate"))
        self.gridLayout_9.addLayout(self.verticalLayout_zCoordinate, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_zCoordinate)
        self.groupBox_Styles = QtGui.QGroupBox(VectorPropertiesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Styles.sizePolicy().hasHeightForWidth())
        self.groupBox_Styles.setSizePolicy(sizePolicy)
        self.groupBox_Styles.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_Styles.setObjectName(_fromUtf8("groupBox_Styles"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_Styles)
        self.gridLayout_8.setContentsMargins(9, 3, 9, 3)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.verticalLayout_Styles = QtGui.QVBoxLayout()
        self.verticalLayout_Styles.setObjectName(_fromUtf8("verticalLayout_Styles"))
        self.gridLayout_8.addLayout(self.verticalLayout_Styles, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_Styles)
        self.groupBox_Features = QtGui.QGroupBox(VectorPropertiesWidget)
        self.groupBox_Features.setObjectName(_fromUtf8("groupBox_Features"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_Features)
        self.verticalLayout_3.setContentsMargins(9, 3, 9, 3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.radioButton_AllFeatures = QtGui.QRadioButton(self.groupBox_Features)
        self.radioButton_AllFeatures.setObjectName(_fromUtf8("radioButton_AllFeatures"))
        self.verticalLayout_3.addWidget(self.radioButton_AllFeatures)
        self.radioButton_IntersectingFeatures = QtGui.QRadioButton(self.groupBox_Features)
        self.radioButton_IntersectingFeatures.setChecked(True)
        self.radioButton_IntersectingFeatures.setObjectName(_fromUtf8("radioButton_IntersectingFeatures"))
        self.verticalLayout_3.addWidget(self.radioButton_IntersectingFeatures)
        self.verticalLayout_Feature = QtGui.QVBoxLayout()
        self.verticalLayout_Feature.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_Feature.setObjectName(_fromUtf8("verticalLayout_Feature"))
        self.checkBox_Clip = QtGui.QCheckBox(self.groupBox_Features)
        self.checkBox_Clip.setChecked(True)
        self.checkBox_Clip.setObjectName(_fromUtf8("checkBox_Clip"))
        self.verticalLayout_Feature.addWidget(self.checkBox_Clip)
        self.verticalLayout_3.addLayout(self.verticalLayout_Feature)
        self.verticalLayout_2.addWidget(self.groupBox_Features)
        self.groupBox_Attrs = QtGui.QGroupBox(VectorPropertiesWidget)
        self.groupBox_Attrs.setObjectName(_fromUtf8("groupBox_Attrs"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_Attrs)
        self.verticalLayout_4.setContentsMargins(9, 3, 9, 3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkBox_ExportAttrs = QtGui.QCheckBox(self.groupBox_Attrs)
        self.checkBox_ExportAttrs.setChecked(False)
        self.checkBox_ExportAttrs.setObjectName(_fromUtf8("checkBox_ExportAttrs"))
        self.verticalLayout_4.addWidget(self.checkBox_ExportAttrs)
        self.formLayout_Label = QtGui.QFormLayout()
        self.formLayout_Label.setContentsMargins(2, -1, 2, -1)
        self.formLayout_Label.setObjectName(_fromUtf8("formLayout_Label"))
        self.label = QtGui.QLabel(self.groupBox_Attrs)
        self.label.setEnabled(False)
        self.label.setMinimumSize(QtCore.QSize(76, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_Label.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox_Label = QtGui.QComboBox(self.groupBox_Attrs)
        self.comboBox_Label.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Label.sizePolicy().hasHeightForWidth())
        self.comboBox_Label.setSizePolicy(sizePolicy)
        self.comboBox_Label.setMaximumSize(QtCore.QSize(270, 16777215))
        self.comboBox_Label.setObjectName(_fromUtf8("comboBox_Label"))
        self.formLayout_Label.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_Label)
        self.verticalLayout_4.addLayout(self.formLayout_Label)
        self.verticalLayout_Label = QtGui.QVBoxLayout()
        self.verticalLayout_Label.setObjectName(_fromUtf8("verticalLayout_Label"))
        self.verticalLayout_4.addLayout(self.verticalLayout_Label)
        self.verticalLayout_2.addWidget(self.groupBox_Attrs)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(VectorPropertiesWidget)
        QtCore.QObject.connect(self.radioButton_IntersectingFeatures, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_Clip.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(VectorPropertiesWidget)

    def retranslateUi(self, VectorPropertiesWidget):
        VectorPropertiesWidget.setWindowTitle(_translate("VectorPropertiesWidget", "Form", None))
        self.label_ObjectType.setText(_translate("VectorPropertiesWidget", "Object type", None))
        self.label_ObjectTypeMessage.setText(_translate("VectorPropertiesWidget", "This type is experimental. Some 3D model files fail to be loaded.", None))
        self.groupBox_zCoordinate.setTitle(_translate("VectorPropertiesWidget", "&Z coordinate", None))
        self.groupBox_Styles.setTitle(_translate("VectorPropertiesWidget", "&Style", None))
        self.groupBox_Features.setTitle(_translate("VectorPropertiesWidget", "&Feature", None))
        self.radioButton_AllFeatures.setText(_translate("VectorPropertiesWidget", "All features", None))
        self.radioButton_IntersectingFeatures.setText(_translate("VectorPropertiesWidget", "Features that intersect with map canvas extent", None))
        self.checkBox_Clip.setText(_translate("VectorPropertiesWidget", "Clip geometries", None))
        self.groupBox_Attrs.setTitle(_translate("VectorPropertiesWidget", "&Attribute and label", None))
        self.checkBox_ExportAttrs.setText(_translate("VectorPropertiesWidget", "Export attributes", None))
        self.label.setText(_translate("VectorPropertiesWidget", "Label field", None))