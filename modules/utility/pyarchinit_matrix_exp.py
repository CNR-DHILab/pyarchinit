# -*- coding: utf-8 -*-
"""
/***************************************************************************
    pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
    stored in Postgres
    -------------------
    begin                : 2018-04-24
    copyright            : (C) 2018 by Salvatore Larosa
    email                : lrssvtml (at) gmail (dot) com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import subprocess
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
import datetime
from datetime import date
from graphviz import Digraph, Source
from .pyarchinit_OS_utility import Pyarchinit_OS_Utility
from ..db.pyarchinit_db_manager import Pyarchinit_db_management
from ...tabs.pyarchinit_setting_matrix import *
class HarrisMatrix:
    HOME = os.environ['PYARCHINIT_HOME']
    DB_MANAGER = ""
    TABLE_NAME = 'us_table'
    MAPPER_TABLE_CLASS = "US"
    ID_TABLE = "id_us"
    MATRIX = Setting_Matrix()
    #s=pyqtSignal(str)
    def __init__(self, sequence,negative, periodi):
        self.sequence = sequence
        self.negative = negative
        self.periodi=periodi
        
    @property
    def export_matrix(self):
        dialog = Setting_Matrix()
        
        dialog.exec_()
        
        
        G = Digraph(engine='dot',strict=False)
        
        G.graph_attr['splines'] = 'ortho'
        G.graph_attr['dpi'] = '300'
        
        
        elist1 = []
        elist2 = []
        elist3 = []
        elist4 = []
        elist5 = []
        elist6 = []
        elist7 = []
        elist8 = []
        elist9 = []
        for i in self.sequence:
            a = (i[0], i[1])
            elist1.append(a)
        
        with G.subgraph(name='main') as e:
           
            e.edges(elist1)
            
            e.node_attr['shape'] = str(dialog.combo_box_3.currentText())
            e.node_attr['style'] = str(dialog.combo_box_4.currentText())
            e.node_attr.update(style='filled', fillcolor=str(dialog.combo_box.currentText()))
            e.node_attr['color'] = 'black'    
            e.node_attr['penwidth'] = str(dialog.combo_box_5.currentText())
            e.edge_attr['penwidth'] = str(dialog.combo_box_5.currentText())
            e.edge_attr['style'] = str(dialog.combo_box_10.currentText())
            e.edge_attr.update(arrowhead=str(dialog.combo_box_11.currentText()), arrowsize=str(dialog.combo_box_12.currentText()))
            for i in self.negative:
                a = (i[0], i[1])
                elist2.append(a)
            
            with G.subgraph(name='main2') as a:
               
                a.edges(elist2)
                
                a.node_attr['shape'] = str(dialog.combo_box_6.currentText())
                a.node_attr['style'] = str(dialog.combo_box_8.currentText())
                a.node_attr.update(style='filled', fillcolor=str(dialog.combo_box_2.currentText()))
                a.node_attr['color'] = 'red'    
                a.node_attr['penwidth'] = str(dialog.combo_box_7.currentText())
                a.edge_attr['penwidth'] = str(dialog.combo_box_7.currentText())
                a.edge_attr['style'] = str(dialog.combo_box_15.currentText())
                a.edge_attr.update(arrowhead=str(dialog.combo_box_14.currentText()), arrowsize=str(dialog.combo_box_16.currentText()))    
        
        for i in self.periodi:
            with G.subgraph(name=i[1]) as c:
                
                for n in i[0]:
                    c.attr('node', shape='box', label =str(n))
                    
                    c.node(str(n))
                
                c.attr(color='blue')
                c.attr('node', shape='box', fillcolor='white', style='filled', gradientangle='90',label=i[2])
                
                c.node(i[2])
               
               
        
        dt = datetime.datetime.now()
        matrix_path = '{}{}{}'.format(self.HOME, os.sep, "pyarchinit_Matrix_folder")
        filename = ('%s_%s_%s_%s_%s_%s_%s') % (
        'Harris_matrix', dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
        f = open(filename, "w")
        
        G.format = 'dot'
        dot_file = G.render(directory=matrix_path, filename=filename)
        
        # For MS-Windows, we need to hide the console window.
        if Pyarchinit_OS_Utility.isWindows():
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE

        #cmd = ' '.join(['tred', dot_file])
        #dotargs = shlex.split(cmd)

        with open(os.path.join(matrix_path, filename + '_tred.dot'), "w") as out, \
                open(os.path.join(matrix_path, 'matrix_error.txt'), "w") as err:
            subprocess.Popen(['tred',dot_file],
                             #shell=True,
                             stdout=out,
                             stderr=err)
                             #startupinfo=si if Pyarchinit_OS_Utility.isWindows()else None)

        tred_file = os.path.join(matrix_path, filename + '_tred.dot')
        
        f = Source.from_file(tred_file, format='svg')
        f.render()
        g = Source.from_file(tred_file, format='jpg')
        g.render()
        return g,f
        # return f
