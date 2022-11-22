from dataclasses import dataclass


class Template:
    
    PROFILE= '''
             select
                distinct p.email as CORREO,
                p.id as PROFILE_ID,
                p."role" as rol,
                p."createdAt"::date as FECHA, 
                unaccent(trim(initcap(p.mayor))) as PROGRAMA,
                i."slug" as IES,
                coalesce (s."seguidores",0) as SEGUIDORES
            from
                profile p join institution i ON
                i.id =p."belongsToId"
                left join seguidores s on s."profileId_2"=p.id
            where
                lower(p."lastName") not like '%booklick%'
                and lower(p."email") not like '%booklick%'
            group by
                  p."createdAt",
                  p.id,
                  p."role",
                  i."slug" ,
                  p.email,
                  unaccent(trim(initcap(p.mayor))),
                  s."seguidores" '''
    LOGIN= '''
                select 
                    "user" as CORREO,
                     "createdAt"::date as FECHA,
                     "env" as IES
                from
                    login l 
                where "env" in ({})
                                '''
    REDIRECT='''
                SELECT 
                    r.id,
                    "user" as correo, 
                    rp."role" AS rol,
                    unaccent(trim(initcap(rp.mayor))) as PROGRAMA,
                    r.slug, 
                    r."createdAt" as fecha,
                    env as ies
                    FROM 
                        redirect r join remote_profile2 rp 
                        on rp.email = r."user" '''

    CONTENT='''
                with redirects as (
                    select 
                        distinct on (slug) slug, 
                        count(r.id) as redirects 
                    from redirect r
                    group by 
                        slug
                    )
                select 
                    rp.email as correo,
                    rp."role" as rol,
                    initcap(trim(unaccent(rp.mayor))) as programa,
                    rc."createdAt" ::date as fecha,
                    rc.title as titulo,
                    rct."label" as tipo,
                    rp.slug as ies,
                    red.redirects as redirecciones
                from remote_profile2 rp join
                     remote_content1 rc on rc.author = rp.email left join 
                     remote_content_type rct on rct.id =rc."type" left join 
                     redirects red on red.slug=rc.slug '''

    LMS =  '''   
                SELECT 
                    el.id,
                    el."email" as correo, 
                    rp."role" AS rol,
                    el."type" as tipo,
                    el."contentSlug" as content_slug,
                    unaccent(trim(initcap(rp.mayor))) as PROGRAMA,
                    el."institutionSlug" as ies,
                    el."createdAt"::date as fecha
                FROM 
                        "eventLti" el  join remote_profile2 rp 
                        on rp.email = el.email '''

    SEARCH= '''SELECT 
                    s.id,
                     unaccent(s.term) as termino,
                    s."user" as correo, 
                    rp."role" AS rol,
                    unaccent(trim(initcap(rp.mayor))) as PROGRAMA,
                    s."env" as ies,
                    s."createdAt"::date as fecha
              FROM 
                    "search" s  join remote_profile2 rp 
                    on rp.email = s."user" '''

    PROXY= '''SELECT 
                p.id, 
                p.email  as correo, 
                rp."role" AS rol,
                unaccent(trim(initcap(rp.mayor))) as programa,
                p.institution  as ies,
                p."type" as tipo,
                p."session" as sesión,
                p."createdAt"::date  as fecha
            FROM 
                    "Proxies" p  join remote_profile_1  rp 
                    on rp.email = p.email '''

@dataclass
class Query:
    template:Template
    param:str=''
    
    @property
    def compile_query(self)->str:
        return self.template.format(self.param)