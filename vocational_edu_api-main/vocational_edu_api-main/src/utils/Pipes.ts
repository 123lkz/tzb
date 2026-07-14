import { Joi } from '@havenzhang/clover'
import { Injectable, PipeTransform } from '@nestjs/common'
import { UnprocessableEntityException } from '@nestjs/common/exceptions/unprocessable-entity.exception'

@Injectable()
export class DatePipe implements PipeTransform<string, string> {
  transform(value: string) {
    const schema = Joi.date().required()
    const { error } = schema.validate(value)
    if (error) {
      throw new UnprocessableEntityException(error, {
        cause: {
          type: error.details[0].type,
          path: error.details[0].path
        }
      })
    }
    return value
  }
}
