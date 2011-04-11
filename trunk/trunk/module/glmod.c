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
    PyObject *tuple = PyTuple_GetItem(args, 0);
    int i, j;
    unsigned int texid, offset;
    PyObject *layer= NULL;
    
    entries.clear();

    VBO = PyInt_AsLong(PyTuple_GetItem(tuple, 0));
    stride = PyInt_AsLong(PyTuple_GetItem(tuple, 1));

    for(i = 2; i < PyTuple_Size(tuple); i++)
    {
        entries.push_back(std::vector<VBOEntry>());
        layer = PyTuple_GetItem(tuple, i);
        for(j = 0; j < PyTuple_Size(layer); j += 2)
        {
            texid = PyInt_AsLong(PyTuple_GetItem(layer, j));
            offset = PyInt_AsLong(PyTuple_GetItem(layer, j+1));
            
            entries[i-2].push_back(VBOEntry(texid, offset));
        }
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_insertVBOlayer(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GetItem(args, 0);
    int j;
    unsigned int texid, offset, insertBeforeLayer;

    insertBeforeLayer = PyInt_AsLong(PyTuple_GetItem(tuple, 0));
    
    entries.insert(entries.begin() + insertBeforeLayer, std::vector<VBOEntry>());

    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AsLong(PyTuple_GetItem(tuple, j));
        offset = PyInt_AsLong(PyTuple_GetItem(tuple, j+1));
        
        entries[insertBeforeLayer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_setVBOlayer(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GetItem(args, 0);
    int j;
    unsigned int texid, offset, layer;

    layer = PyInt_AsLong(PyTuple_GetItem(tuple, 0));
    entries[layer].clear();

    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AsLong(PyTuple_GetItem(tuple, j));
        offset = PyInt_AsLong(PyTuple_GetItem(tuple, j+1));
        
        entries[layer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_addVBOentry(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GetItem(args, 0);
    int j;
    unsigned int texid, offset, layer;

    layer = PyInt_AsLong(PyTuple_GetItem(tuple, 0));

    for(j = 1; j < PyTuple_Size(tuple); j += 2)
    {
        texid = PyInt_AsLong(PyTuple_GetItem(tuple, j));
        offset = PyInt_AsLong(PyTuple_GetItem(tuple, j+1));
        
        entries[layer].push_back(VBOEntry(texid, offset));
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_generateTexture(PyObject *self, PyObject* args)
{
    int w, h, ok;
    unsigned int texid;
    const char *pixels;

    ok = PyArg_ParseTuple(args, "iis", &w, &h, &pixels);

    texid = -1;
    glGenTextures(1, &texid);
    glBindTexture(extension, texid);

    glTexParameteri(extension, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(extension, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(extension, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(extension, GL_TEXTURE_MIN_FILTER, GL_LINEAR);

    //'''possibly GL_COMPRESSED_RGBA_ARB as third parameter'''
    glTexImage2D(extension, 0, GL_RGBA, w, h, 
                 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);

    return PyInt_FromLong(texid);
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

static PyObject * glmod_clear(PyObject *self, PyObject* args)
{
    glClear(GL_COLOR_BUFFER_BIT);
    return PyInt_FromLong(0L);
}

static PyMethodDef GLModMethods[] = {
    {"drawTexture",  glmod_drawTexture, METH_VARARGS, "draw a texture"},
    {"drawVBO",  glmod_drawVBO, METH_VARARGS, "draw the list of texids with VBO"},
    {"setVBO",  glmod_setVBO, METH_VARARGS, "erase & set the list of VBO entries"},
    {"insertVBOlayer",  glmod_insertVBOlayer, METH_VARARGS, "add a layer of VBO entries"},
    {"setVBOlayer",  glmod_setVBOlayer, METH_VARARGS, "erase & set a layer of VBO entries"},
    {"addVBOentry",  glmod_addVBOentry, METH_VARARGS, "add an entry to a layer"},
    {"generateTexture",  glmod_generateTexture, METH_VARARGS, "generate texture id"},
    {"clear",  glmod_clear, METH_VARARGS, "clear"},
    {"init",  glmod_init, METH_VARARGS, "init"},
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


