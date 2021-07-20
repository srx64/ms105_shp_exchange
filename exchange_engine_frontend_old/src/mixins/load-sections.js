import {camelCase, upperFirst} from 'lodash'

export default function (sections = []) {
  return {
    name: 'LoadSections',

    components: sections.reduce((acc, cur) => {
      const name = upperFirst(camelCase(cur))

      acc[`Section${name}`] = () => import(`@/components/home/sections/${name}.vue`)

      return acc
    }, {}),

    data: () => ({ sections }),
  }
}