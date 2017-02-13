//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  This program derives from OpenSees <http://opensees.berkeley.edu>
//  developed by the  «Pacific earthquake engineering research center».
//
//  Except for the restrictions that may arise from the copyright
//  of the original program (see copyright_opensees.txt)
//  XC is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or 
//  (at your option) any later version.
//
//  This software is distributed in the hope that it will be useful, but 
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. 
//
//
// You should have received a copy of the GNU General Public License 
// along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------


#include "BidimStrainLoad.h"
#include "utility/matrix/Vector.h"
#include "utility/matrix/ID.h"


#include "utility/actor/actor/MovableVectors.h"
#include "utility/actor/actor/MovableVector.h"
#include "utility/matrix/Matrix.h"


XC::BidimStrainLoad::BidimStrainLoad(int tag, const std::vector<Vector> &t,const ID &theElementTags)
  :BidimLoad(tag, LOAD_TAG_BidimStrainLoad, theElementTags), deformaciones(t) {}
XC::BidimStrainLoad::BidimStrainLoad(int tag,const size_t &sz,const Vector &t,const ID &theElementTags)
  :BidimLoad(tag, LOAD_TAG_BidimStrainLoad, theElementTags), deformaciones(sz,t) {}

XC::BidimStrainLoad::BidimStrainLoad(int tag,const size_t &sz, const ID &theElementTags)
  :BidimLoad(tag, LOAD_TAG_BidimStrainLoad, theElementTags), deformaciones(sz) {}

XC::BidimStrainLoad::BidimStrainLoad(int tag,const size_t &sz, const Vector &t)
  :BidimLoad(tag, LOAD_TAG_BidimStrainLoad), deformaciones(sz,t) {}

XC::BidimStrainLoad::BidimStrainLoad(int tag,const size_t &sz)
  :BidimLoad(tag, LOAD_TAG_BidimStrainLoad), deformaciones(sz) {}

XC::BidimStrainLoad::BidimStrainLoad(const size_t &sz)
  :BidimLoad(0,LOAD_TAG_BidimStrainLoad), deformaciones(sz) {}

//! @brief Asigna el valor de la deformación de uno de los puntos de Gauss.
//! el primer índice es el del punto de gauss y el segundo la dirección de
//! la deformación.
void XC::BidimStrainLoad::setStrainComp(const size_t &i,const size_t &j,const double &strain)
  {
    if(i<deformaciones.size())
      {
        Vector &def= deformaciones.at(i);
        if(j<size_t(def.Size()))
          def(j)= strain;
        else
          std::cerr << nombre_clase() << "::setStrainComp "
                    << " no existe la componente del vector deformación de índice: "
                    << j << "." << std::endl;
      }
    else
      std::cerr << nombre_clase() << "::setStrainComp "
                << " no existe el punto de Gauss de índice: "  << i
                << std::endl;
  }

//! @brief Asigna las deformaciones.
void XC::BidimStrainLoad::setDeformaciones(const Matrix &def)
  {
    const int nRows= def.noRows();
    const int nCols= def.noCols();
    std::vector<Vector> tmp(nRows);
    Vector ri(nCols);
    for(int i= 0;i<nRows;i++)
      {
        for(int j= 0;j<nCols;j++)
          ri[j]= def(i,j);
        tmp[i]= ri;
      }
    deformaciones= tmp;
  }


//! @brief Returns a vector para almacenar los dbTags
//! de los miembros de la clase.
XC::DbTagData &XC::BidimStrainLoad::getDbTagData(void) const
  {
    static DbTagData retval(6);
    return retval;
  }

//! @brief Envía los datos through the channel being passed as parameter.
int XC::BidimStrainLoad::sendData(CommParameters &cp)
  {
    int res= BidimLoad::sendData(cp);
    res+= cp.sendVectors(deformaciones,getDbTagData(),CommMetaData(5));
    return res;
  }

//! @brief Recibe los datos through the channel being passed as parameter.
int XC::BidimStrainLoad::recvData(const CommParameters &cp)
  {
    int res= BidimLoad::recvData(cp);
    res+= cp.receiveVectors(deformaciones,getDbTagData(),CommMetaData(5));
    return res;
  }

int XC::BidimStrainLoad::sendSelf(CommParameters &cp)
  {
    inicComm(6);
    int res= sendData(cp);

    const int dataTag= getDbTag(cp);
    res+= cp.sendIdData(getDbTagData(),dataTag);
    if(res<0)
      std::cerr << "BidimStrainLoad::sendSelf() - failed to send data\n";    
    return res;
  }

int XC::BidimStrainLoad::recvSelf(const CommParameters &cp)
  {
    inicComm(6);
    const int dataTag= getDbTag();
    int res= cp.receiveIdData(getDbTagData(),dataTag);
    if(res<0)
      std::cerr << "TrussStrainLoad::recvSelf() - data could not be received\n" ;
    else
      res+= recvData(cp);
    return res;
  }

void XC::BidimStrainLoad::Print(std::ostream &s, int flag) const
  {
    s << "BidimStrainLoad" << std::endl;
    if(!deformaciones.empty())
      {
        std::vector<Vector>::const_iterator i= deformaciones.begin();
        s << *i;
        for(;i!=deformaciones.end();i++)
          s << ", " << *i;
      }
    BidimLoad::Print(s,flag);
  }

