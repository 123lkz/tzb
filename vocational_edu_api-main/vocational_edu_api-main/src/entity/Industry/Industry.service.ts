import { BadRequestException, Injectable } from '@nestjs/common'
import { IndustryEntity } from './Industry'
import { GradeTreeItem, IndustryDownResult, IndustryUpResult } from './Industry.dto'

@Injectable()
export class IndustryService {
  private static model() {
    return (IndustryEntity as any).model
  }

  static async getGradeList(): Promise<GradeTreeItem[]> {
    const Model = this.model()

    // 从 level 2 开始查询，忽略 level 1，支持到 level 5
    const docs = (await Model.find({ level: { $in: [2, 3, 4, 5] } })
      .select('code name level parent_code')
      .lean()) as Array<{
      code: string
      name: string
      level: 2 | 3 | 4 | 5
      parent_code?: string
      children?: any[]
    }>

    const byCode = new Map<
      string,
      { code: string; name: string; level: 2 | 3 | 4 | 5; parent_code?: string; children?: any[] }
    >()
    docs.forEach((d) => byCode.set(d.code, d))

    docs.forEach((d) => (d.children = []))

    const roots: Array<{
      code: string
      name: string
      level: 2 | 3 | 4 | 5
      parent_code?: string
      children?: any[]
    }> = []
    docs.forEach((d) => {
      // 从 level 2 开始作为根节点
      if (d.level === 2 || !d.parent_code) {
        roots.push(d)
      } else {
        const parent = byCode.get(d.parent_code)
        if (parent) parent.children!.push(d)
      }
    })

    return roots
      .filter((r) => r.level === 2)
      .map((r) => ({
        level: r.level,
        name: r.name,
        code: r.code,
        children: (r.children || []).map((l3: any) => ({
          level: l3.level,
          name: l3.name,
          code: l3.code,
          children: (l3.children || []).map((l4: any) => ({
            level: l4.level,
            name: l4.name,
            code: l4.code,
            children: (l4.children || []).map((l5: any) => ({
              level: l5.level,
              name: l5.name,
              code: l5.code
            }))
          }))
        }))
      }))
  }

  static async getUpByLevel(query: { level: 2 | 3 | 4 | 5; name?: string; code?: string }): Promise<IndustryUpResult> {
    const { level, name, code } = query || ({} as any)
    if (!level) throw new BadRequestException('缺少参数: level')
    if (level < 2) throw new BadRequestException('级别必须从2开始')

    const Model = this.model()
    const match: any = {}
    if (name) match.name = name
    if (code) match.code = code
    if (!name && !code) match.level = level

    const docs = await Model.find(match).select('code name level path').lean()

    const sets: Record<2 | 3 | 4 | 5, Set<string>> = {
      2: new Set<string>(),
      3: new Set<string>(),
      4: new Set<string>(),
      5: new Set<string>()
    }
    const pushToken = (nm?: string, cd?: string, lv?: number) => {
      if (!nm || !cd || !lv) return
      if (lv >= 2 && lv <= 5) sets[lv as 2 | 3 | 4 | 5].add(`${nm}||${cd}`)
    }

    const codesToFetch = new Set<string>()
    docs.forEach((d: any) => {
      pushToken(d.name, d.code, d.level)
      ;(d.path || []).forEach((c: string) => codesToFetch.add(c))
    })

    if (codesToFetch.size > 0) {
      const parents = await Model.find({ code: { $in: Array.from(codesToFetch) } })
        .select('code name level')
        .lean()
      parents.forEach((p: any) => pushToken(p.name, p.code, p.level))
    }

    const toArr = (s: Set<string>) =>
      Array.from(s).map((token) => {
        const [n, c] = token.split('||')
        return { name: n, code: c }
      })

    return {
      dalei: [] as Array<{ name: string; code: string }>, // 忽略 level 1
      zhonglei: toArr(sets[2]),
      xiaoli: toArr(sets[3]),
      xilei: toArr(sets[4]),
      zilei: toArr(sets[5])
    }
  }

  static async getDownByLevel(query: { code?: string; name?: string }): Promise<IndustryDownResult> {
    const { code, name } = query || ({} as any)
    if (!code && !name) throw new BadRequestException('至少需要 code 或 name 之一')

    const Model = this.model()
    // 先定位传入对象
    let current = null as any
    if (code) current = await Model.findOne({ code }).select('code name level path').lean()
    if (!current && name) current = await Model.findOne({ name }).select('code name level path').lean()
    if (!current) return { zilei: [] as Array<{ name: string; code: string }> }

    // 检查级别是否从2开始
    if (current.level < 2) {
      throw new BadRequestException('级别必须从2开始')
    }

    // 准备集合容器
    const zhonglei = new Set<string>()
    const xiaoli = new Set<string>()
    const xilei = new Set<string>()
    const zilei = new Set<string>()
    const push = (s: Set<string>, n: string, c: string) => s.add(`${n}||${c}`)

    // 如果传入的是2级：返回 2/3/4/5 级
    // 如果传入的是3级：返回 3/4/5 级
    // 如果传入的是4级：返回 4/5 级
    // 如果传入的是5级：只返回5级本身
    const lvl = current.level as 2 | 3 | 4 | 5

    // 收集本级
    if (lvl === 2) push(zhonglei, current.name, current.code)
    if (lvl === 3) push(xiaoli, current.name, current.code)
    if (lvl === 4) push(xilei, current.name, current.code)
    if (lvl === 5) push(zilei, current.name, current.code)

    // 如果需要下钻，先找出下一层的直接子节点: level+1, parent_code = current.code
    const collectChildren = async (parentCodes: string[], targetLevel: number) => {
      if (parentCodes.length === 0) return [] as any[]
      return await Model.find({ parent_code: { $in: parentCodes }, level: targetLevel })
        .select('code name level')
        .lean()
    }

    let nextParents: string[] = []
    if (lvl <= 4) {
      // 收集下一级
      const childrenL1 = await collectChildren([current.code], lvl + 1)
      childrenL1.forEach((c: any) => {
        if (c.level === 3) push(xiaoli, c.name, c.code)
        if (c.level === 4) push(xilei, c.name, c.code)
        if (c.level === 5) push(zilei, c.name, c.code)
      })
      nextParents = childrenL1.map((c: any) => c.code)
    }

    if (lvl <= 3) {
      // 收集下二级
      const childrenL2 = await collectChildren(nextParents, lvl + 2)
      childrenL2.forEach((c: any) => {
        if (c.level === 4) push(xilei, c.name, c.code)
        if (c.level === 5) push(zilei, c.name, c.code)
      })
      nextParents = childrenL2.map((c: any) => c.code)
    }

    if (lvl <= 2) {
      // 收集下三级
      const childrenL3 = await collectChildren(nextParents, lvl + 3)
      childrenL3.forEach((c: any) => {
        if (c.level === 5) push(zilei, c.name, c.code)
      })
    }

    const toArr = (s: Set<string>) =>
      Array.from(s).map((t) => {
        const [n, c] = t.split('||')
        return { name: n, code: c }
      })

    return {
      dalei: undefined as Array<{ name: string; code: string }> | undefined, // 忽略 level 1
      zhonglei: lvl <= 2 ? toArr(zhonglei) : undefined,
      xiaoli: lvl <= 3 ? toArr(xiaoli) : undefined,
      xilei: lvl <= 4 ? toArr(xilei) : undefined,
      zilei: toArr(zilei)
    }
  }
}
