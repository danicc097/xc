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
//ElementPtrs.cpp

#include "ElementPtrs.h"
#include "domain/mesh/element/Element.h"
#include "domain/domain/Domain.h"


#include "xc_basic/src/matrices/m_int.h"
#include "utility/matrix/ID.h"


//! @brief Constructor.
XC::ElementPtrs::ElementPtrs(void)
  : theElements(0) {}


//! @brief Destructor.
XC::ElementPtrs::~ElementPtrs(void)
  { theElements.clear(); }

//! @brief Asigna los pointers to partir de los identificadores de elemento.
void XC::ElementPtrs::setPtrs(Domain *theDomain, const ID &theElementTags)
  {
    size_t sz= theElementTags.Size();
    theElements.clear();
    if(theDomain)
      {
        theElements.resize(sz);
        for(size_t i=0; i<sz; i++)
          {
            theElements[i]= theDomain->getElement(theElementTags(i));
            if(!theElements[i])
              {
                std::cerr << "WARNING - XC::ElementPtrs::setDomain - ele with tag ";
	        std::cerr << theElementTags(i) << " does not exist in the domain\n";
              }
          }
      }
  }

//! @brief Returns an iterator al elemento cuyo tag se pasa como parámetro.
XC::ElementPtrs::iterator XC::ElementPtrs::find(const int &tag)
  {
    iterator retval= end();
    for(iterator i= begin();i!=end();i++)
      if((*i)->getTag() == tag)
        retval= i;
    return retval;
  }

//! @brief Returns an iterator al elemento cuyo tag se pasa como parámetro.
XC::ElementPtrs::const_iterator XC::ElementPtrs::find(const int &tag) const
  {
    const_iterator retval= end();
    for(const_iterator i= begin();i!=end();i++)
      if((*i)->getTag() == tag)
        retval= i;
    return retval;
  }

XC::Element *XC::ElementPtrs::findPtr(const int &tag)
  {
    XC::Element *retval= nullptr;
    iterator i= find(tag);
    if(i!=end())
      retval= *i;
    return retval;
  }

const XC::Element *XC::ElementPtrs::findPtr(const int &tag) const
  {
    const XC::Element *retval= nullptr;
    const_iterator i= find(tag);
    if(i!=end())
      retval= *i;
    return retval;
  }


//! @brief Elimina el elemento cuyo tag se pasa como parámetro.
size_t XC::ElementPtrs::removeElement(const int &tag) 
  {
    iterator i= find(tag);
    if(i!=end())
      theElements.erase(i,i);
    return size();
  }



XC::ElementPtrs::const_reference XC::ElementPtrs::operator()(const size_t &i) const
  { return theElements[i]; }
XC::ElementPtrs::reference XC::ElementPtrs::operator()(const size_t &i)
  { return theElements[i]; }
XC::ElementPtrs::const_reference XC::ElementPtrs::operator[](const size_t &i) const
  { return theElements[i]; }
XC::ElementPtrs::reference XC::ElementPtrs::operator[](const size_t &i)
  { return theElements[i]; }
