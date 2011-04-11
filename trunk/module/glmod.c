/*
 * main - starting point of FM
 *
 * By Oipo (kingoipo@gmail.com)
 */

#include <Python.h>
#include <vector>

#define GL_GLEXT_PROTOTYPES 1

#ifdef __APPLE__
    #include <OpenGL/gl.h>
#else
    #ifdef _WIN32
        #undef GL_GLEXT_PROTOTYPES
        #include <GL/gl.h>
        #define WIN32_LEAN_AND_MEAN 1
        #include <windows.h>
        #include "glext.h"
        PFNGLBINDBUFFERPROC glBindBuffer = NULL;
    #else
        #include <GL/gl.h>
    #endif
#endif

#define BUFFER_OFFSET(i) ((char *)NULL + (i))

GLenum extension = GL_TEXTURE_RECTANGLE_ARB;

class VBOEntry
{
    public:
    unsigned int texid, offset;

    VBOEntry(unsigned int texid, unsigned int offset)
    {
        this->texid = texid;
        this->offset = offset;
    }
};

int VBO, stride;
std::vector<std::vector<VBOEntry> > entries;

static PyObject * glmod_drawTexture(PyObject *self, PyObject* args)
{
    int texid, ok;
    float x, y, w, h, cx, cy, cw, ch;

    ok = PyArg_ParseTuple(args, "iffffffff", &texid, &x, &y, &w, &h, &cx, &cy, &cw, &ch);

    if(!ok)
       return PyInt_FromLong(-1L); 

    glBindTexture(extension, texid);

    glBegin(GL_QUADS);
    //Top-left vertex (corner)
    glTexCoord2f(cx, cy+ch); //image/texture
    glVertex3f(x, y, 0); //_screen coordinates

    //Bottom-left vertex (corner)
    glTexCoord2f(cx+cw, cy+ch);
    glVertex3f(x+w, y, 0);

    //Bottom-right vertex (corner)
    glTexCoord2f(cx+cw, cy);
    glVertex3f(x+w, y+h, 0);

    //Top-right vertex (corner)
    glTexCoord2f(cx, cy);
    glVertex3f(x, y+h, 0);
    glEnd();

    return PyInt_FromLong(0L);
}

static PyObject * glmod_drawVBO(PyObject *self, PyObject* args)
{
    int i, k, lastid = -1;

    glBindBuffer(GL_ARRAY_BUFFER_ARB, VBO);
    glTexCoordPointer(2, GL_FLOAT, stride, 0);
    glVertexPointer(2, GL_FLOAT, stride, BUFFER_OFFSET(stride/2));

    glEnableClientState(GL_VERTEX_ARRAY);
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);

    for(i = 0; i < entries.size(); i++)
    {
        for(k = 0; k < entries[i].size(); k++)
        {
            if(lastid != entries[i][k].texid)
            {
                glBindTexture(extension, entries[i][k].texid);
                lastid = entries[i][k].texid;
            }

            glDrawArrays(GL_QUADS, entries[i][k].offset, 4);
        }
    }

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER_ARB, 0);

    return PyInt_FromLong(0L);
}

static PyObject * glmod_setVBO(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GET_ITEM(args, 0);
    int i, j;
    unsigned int texid, offset;
    PyObject *layer= NULL;
    
    entries.clear();

    for(i = 0; i < PyTuple_Size(tuple); i++)
    {
        entries.push_back(std::vector<VBOEntry>());
        layer = PyTuple_GET_ITEM(tuple, i);
        for(j = 0; j < PyTuple_Size(layer); j += 2)
        {
            texid = PyInt_AS_LONG(PyTuple_GET_ITEM(layer, j));
            offset = PyInt_AS_LONG(PyTuple_GET_ITEM(layer, j+1));
            
            entries[i].push_back(VBOEntry(texid, offset));
        }
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_insertVBOlayer(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GET_ITEM(args, 0);
    int j;
    unsigned int texid, offset, insertBeforeLayer;

    insertBeforeLayer = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, 0));
    
    if(insertBeforeLayer >= entries.size())
        entries.push_back(std::vector<VBOEntry>());
    else
        entries.insert(entries.begin() + insertBeforeLayer, std::vector<VBOEntry>());

    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j));
        offset = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j+1));
        //printf("adding %i at %i on %i\r\n", texid, offset, insertBeforeLayer);
        
        entries[insertBeforeLayer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_setVBOlayer(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GET_ITEM(args, 0);
    int j;
    unsigned int texid, offset, layer;

    layer = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, 0));
#ifdef DEBUG
    if(layer > entries.size())
    {
        printf("SetLayer Layer too high\r\n");
        return PyInt_FromLong(-1L);
    }
#endif
    entries[layer].clear();

    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j));
        offset = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j+1));
        
        entries[layer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_addVBOentry(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GET_ITEM(args, 0);
    int j;
    unsigned int texid, offset, layer;

    layer = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, 0));
#ifdef DEBUG
    if(layer > entries.size())
    {
        printf("AddEntry Layer too high\r\n");
        return PyInt_FromLong(-1L);
    }
#endif
    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j));
        offset = PyInt_AS_LONG(PyTuple_GET_ITEM(tuple, j+1));
        
        entries[layer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_drawLines(PyObject *self, PyObject* args)
{
    PyObject *dict = PyTuple_GET_ITEM(args, 0);
    int prevthickness = 0, thickness, i = 0;
    
    PyObject *key, *values, *value, *test;
    Py_ssize_t pos = 0;

    glBegin(GL_LINES);
    while (PyDict_Next(dict, &pos, &key, &values)) {
        thickness = PyInt_AS_LONG(key);
        if(thickness != prevthickness)
        {
            glEnd();
            glLineWidth(thickness);
            prevthickness = thickness;
            glBegin(GL_LINES);
        }
#ifdef DEBUG
        if(!PyList_Check(values))
        {
            printf("values not a list\r\n");
            return PyInt_FromLong(0L);
        }
#endif
        for(i = 0; i < PyList_Size(values); i++)
        {
            value = PyList_GET_ITEM(values, i);
#ifdef DEBUG
            if(!PyTuple_Check(value))
            {
                printf("value not a tuple\r\n");
                return PyInt_FromLong(0L);
            }
            if(!PyFloat_Check(PyTuple_GET_ITEM(value, 0)))
            {
                printf("x not a tuple\r\n");
                return PyInt_FromLong(0L);
            }
#endif
            double x = PyFloat_AS_DOUBLE(PyTuple_GET_ITEM(value, 0));
            double y = PyFloat_AS_DOUBLE(PyTuple_GET_ITEM(value, 1));
            double w = PyFloat_AS_DOUBLE(PyTuple_GET_ITEM(value, 2));
            double h = PyFloat_AS_DOUBLE(PyTuple_GET_ITEM(value, 3));
            glVertex2d(x, y);
            glVertex2d(w, h);
        }
    }
    glEnd();

    return PyInt_FromLong(0L);
}

static PyObject * glmod_initVBO(PyObject *self, PyObject* args)
{
    int ok;
    ok = PyArg_ParseTuple(args, "ii", &VBO, &stride);

    if(!ok)
        return PyInt_FromLong(-1L); //Parse error
    return PyInt_FromLong(0L);
}

static PyObject * glmod_init(PyObject *self, PyObject* args)
{
    int ok;

    ok = PyArg_ParseTuple(args, "i", &extension);

    if(!ok)
        return PyInt_FromLong(-1L); //Parse error

#ifdef _WIN32
    glBindBuffer = (PFNGLBINDBUFFERARBPROC)wglGetProcAddress("glBindBufferARB");
    if(glBindBuffer == NULL)
        return PyInt_FromLong(-2L); //Init went ok, but couldn't get glBindBuffer
#endif

    return PyInt_FromLong(0L);
}

static PyMethodDef GLModMethods[] = {
    {"drawTexture",  glmod_drawTexture, METH_VARARGS, "draw a texture"},
    {"drawVBO",  glmod_drawVBO, METH_VARARGS, "draw the list of texids with VBO"},
    {"setVBO",  glmod_setVBO, METH_VARARGS, "erase & set the list of VBO entries"},
    {"insertVBOlayer",  glmod_insertVBOlayer, METH_VARARGS, "add a layer of VBO entries"},
    {"setVBOlayer",  glmod_setVBOlayer, METH_VARARGS, "erase & set a layer of VBO entries"},
    {"addVBOentry",  glmod_addVBOentry, METH_VARARGS, "add an entry to a layer"},
    {"drawLines",  glmod_drawLines, METH_VARARGS, "draws lines from a dict"},
    {"init",  glmod_init, METH_VARARGS, "init"},
    {"initVBO",  glmod_initVBO, METH_VARARGS, "initVBO"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC initglmod(void)
{
    PyObject *m;
    PyImport_AddModule("glmod");
    m = Py_InitModule("glmod", GLModMethods);
    if (m == NULL)
        return;
}


