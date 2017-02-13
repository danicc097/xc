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

#include "DqPtrsConstraint.h"
#include "domain/constraints/Constraint.h"
#include "preprocessor/cad/trf/TrfGeom.h"
#include "xc_basic/src/funciones/algebra/ExprAlgebra.h"


//! @brief Constructor.
XC::DqPtrsConstraint::DqPtrsConstraint(EntCmd *owr)
  : DqPtrs<Constraint>(owr) {}

//! @brief Constructor de copia.
XC::DqPtrsConstraint::DqPtrsConstraint(const std::deque<Constraint *> &ts)
  : DqPtrs<Constraint>(ts) {}

//! @brief Constructor de copia.
XC::DqPtrsConstraint::DqPtrsConstraint(const std::set<const Constraint *> &st)
  : DqPtrs<Constraint>()
  {
    std::set<const Constraint *>::const_iterator k;
    k= st.begin();
    for(;k!=st.end();k++)
      push_back(const_cast<Constraint *>(*k));
  }

//! @brief Returns (if it exists) a pointer al elemento
//! cuyo tag se pasa como parámetro.
XC::Constraint *XC::DqPtrsConstraint::buscaConstrainto(const int &tag)
  {
    Constraint *retval= nullptr;
    Constraint *tmp= nullptr;
    for(iterator i= begin();i!=end();i++)
      {
        tmp= *i;
        if(tmp)
          {
            if(tag == tmp->getTag())
              {
                retval= tmp;
                break;
              }
          }
      }
    return retval;
  }

//! @brief Returns (if it exists) a pointer al elemento
//! cuyo tag se pasa como parámetro.
const XC::Constraint *XC::DqPtrsConstraint::buscaConstrainto(const int &tag) const
  {
    const Constraint *retval= nullptr;
    const Constraint *tmp= nullptr;
    for(const_iterator i= begin();i!=end();i++)
      {
        tmp= *i;
        if(tmp)
          {
            if(tag == tmp->getTag())
              {
                retval= tmp;
                break;
              }
          }
      }
    return retval;
  }

//!  @brief Asigna índices a los objetos de la lista para poder emplearlos en VTK.
void XC::DqPtrsConstraint::numera(void)
  {
    size_t idx= 0;
    for(iterator i= begin();i!=end();i++,idx++)
      {
	Constraint *ptr= *i;
        ptr->set_indice(idx);
      }
  }

//! @brief Returns the tags de los elementos.
std::set<int> XC::DqPtrsConstraint::getTags(void) const
  {
    std::set<int> retval;
    for(const_iterator i= begin();i!=end();i++)
      retval.insert((*i)->getTag());
    return retval;
  }
