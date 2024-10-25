from sqlalchemy import asc, desc, or_
from app.models.sensor import Sensor
from app.schemas.sensor_schema import SensorSchema
from db import db
from app.utils.success_responses import pagination_response,created_ok_message,ok_message
from app.utils.error.error_responses import bad_request_message,server_error_message
from marshmallow import ValidationError
from app.services.wetland_service import get_wetland_by_id
sensor_schema = SensorSchema()
sensor_schema_many = SensorSchema(many=True)

def get_all_sensors(pagelink,statusList,typesList):
    try:
        
        query = Sensor.query

        query = apply_filters_and_pagination(query, text_search = pagelink.text_search,sort_order=pagelink.sort_order, statusList=statusList, typesList=typesList)
        
        sensors_paginated = query.paginate(page=pagelink.page, per_page=pagelink.page_size, error_out=False)

        data = sensor_schema_many.dump(sensors_paginated)
        
        return pagination_response(sensors_paginated.total,sensors_paginated.pages,sensors_paginated.page,sensors_paginated.per_page,data=data)
    except Exception as e:
        raise Exception(str(e))



def get_sensor_by_id(sensor_id):
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise ValueError("Sensor not found")
        return (sensor_schema.dump(sensor))
    except ValueError as e:
        raise ValueError("Sensor not found")
    
def create_sensor(data):
    try:
        
        db.session.add(data)
        db.session.commit()
        return created_ok_message(message="El Sensor ha sido creado correctamente!")
    except Exception as err:
        db.session.rollback()
        return server_error_message(details=str(err))

def update_sensor(sensor_id, data):
    try:
        if not  get_wetland_by_id(data.get('wetland_id')):
            raise Exception("golasd")
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise ValueError("Sensor not found")
        sensor = sensor_schema.load(data, instance=sensor, partial=True)
        db.session.commit()
        return ok_message()
    except ValueError as err:
        raise ValueError(err)
    except Exception as e:
        db.session.rollback()
        raise Exception(str(e)) 

def delete_sensor(sensor_id):
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise ValueError("Sensor not found")
        db.session.delete(sensor)
        db.session.commit()
        return True
    except ValueError as err:
        db.session.rollback()
        raise ValueError("Sensor not found")
    except Exception as e:
        db.session.rollback()
        raise Exception(str(e))

def apply_filters_and_pagination(query, text_search=None, sort_order=None, statusList=None,typesList=None):
    
    
    if typesList:
        query = query.filter(or_(
            typesList == None,
            Sensor.type_sensor.in_(typesList)
        ))

    if statusList:
        query = query.filter(or_(
            statusList == None,
            Sensor.status.in_(statusList)
        ))
    


    if text_search:
       
        search_filter = or_(
            Sensor.name.ilike(f'%{text_search}%')
        )
        query = query.filter(search_filter)

    
    if sort_order.property_name:
        if sort_order.direction == 'ASC':
            query = query.order_by(asc(sort_order.property_name))
        else:
            query = query.order_by(desc(sort_order.property_name))

    return query


