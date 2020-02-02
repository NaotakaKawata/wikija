# -*- coding: utf-8 -*-

require 'json'
require 'kyotocabinet'
require_relative 'candiate_lookupper.rb'
require_relative 'feature_extraction_for_ranking.rb'

class DisambiguateStrategyBase
  def disambiguate(candidates, context)
    return nil
  end
end

class MostFrequentDisambiguator < DisambiguateStrategyBase
  def initialize(kb_filename)
  end
  def disambiguate(candidates, context, k_best=5)
    #p candidates
    return candidates.sort_by{|e| -e["p_e_x"]}.first(5)
  end
end

class CosineSimDisambiguator < DisambiguateStrategyBase
  def initialize(kb_filename)
    @kb = KyotoCabinet::DB::new
    @kb.open(kb_filename, KyotoCabinet::DB::OREADER)
  end
  def disambiguate(candidates, context, k_best=5)
    candidates.each do |cand|

    end
  end
end

class Linker

  def initialize(cg_filename, kb_filename, strategy)
    @cg = CandidateLookupper.new(cg_filename)
    @disambiguator = strategy.new(kb_filename)
  end

  def disambiguate(mention, context=nil)
    candidates = @cg.lookup(mention)
    return nil unless candidates
    rankedlist = @disambiguator.disambiguate(candidates["candidates"], context)
    return rankedlist
  end
end

class LinkerModel
  def initialize(weight_filename, idf_filename)
    open(weight_filename) do |f|
      l = f.gets()
      @weights = l.split(/\s/).map(&:to_f)
    end
    #p @weights
    @metrics = []
    @metrics << GlobalBoWSimilarity.new(idf_filename)
    @metrics << StringSimilarity.new()
    @metrics << EntityPopularity.new()
  end

  def calc_score(doc, mention, entity, e)
    sum = 0.0
    sum += @weights[0]
    @metrics.each.with_index do |metric, i|
      if @weights[i+1] != 0.0
        sum += (@weights[i+1] || 0.0) * metric.calc(doc, mention, entity, e)
      end
    end
    return sum
  end
end

if __FILE__ == $0
  require 'logger'
  require 'optparse'

  at_exit{ #linker.teardown()
  }

  params = ARGV.getopts("c:k:f:v:m:t:T:")

  @from = (params['f'] || 'extracted').to_s
  @to   = (params['t'] || 'linked').to_s

  cg_filename = (params['c'] || 'data/master06_candidates.kct')
  kb_filename = (params['k'] || 'data/master06_content.kch')
  idf_filename      = params['i'] || 'data/master06_content_mecab_annotated.idf.kch'
  model_filename    = (params['m'] || 'data/linker.model')

  TH = (params['T'] || 0.0).to_f
  TH_CANDIDATE = 0.05

  require_relative 'candiate_lookupper.rb'
  @cg = CandidateLookupper.new(cg_filename)
  @kb = CandidateLookupper.new(kb_filename)
  linker = LinkerModel.new(model_filename, idf_filename)

  while line=gets()
    o = JSON.load(line)
    o['ner'][@to] = []
    # o['ner']['extracted']
    # o['ner']['chunk']
    # o['ner']['gold']
    o['ner'][@from].each do |sentence|
      linked = []
      sentence.each do |mention|
        surface = mention.first
        candidates =  @cg.lookup(surface)
        #p candidates
        unless candidates
          linked  << {"surface" => surface, "title" => "NIL"}
          next
        end
        scores = candidates['candidates'].select{|e| e['p_e_x'] > TH_CANDIDATE }.map{ |e|
          ee = @kb.lookup(e['title'])
          s = linker.calc_score(o, surface, ee, e)
          {"surface" => surface, "title" => ee['entry'], "score" => s.round(3) ,"wikipedia_ID" => ee['wikipedia_ID']}
        }
        cand = scores.max_by {|e| e['score'] }
        #linked = cand["title"]
        if cand['title'] == nil
	        linked << {"surface" => surface, "title" => "NIL"}
        elsif cand['score'] < TH
                linked << {"surface" => surface, "title" => "NIL"}
        else
	        linked << {"surface" => surface, "title" => cand['wikipedia_ID']}
        end
        #if cand['score'] < TH
        #  linked << {"surface" => surface, "title" => nil, "score" => 0.0}
        #else
        #  linked << cand
        #end
      end
      o['ner'][@to] << linked
    end
    puts o.to_json
  end

  #  o['ner']['linked'] = o['ner']['extracted'].dup
  #  o['ner']['extracted'].each.with_index do |sentence, i|
  #    sentence.each.with_index do |mention, j|
  #      o['ner']['linked'][i][j] << linker.disambiguate(mention[0])
  #    end
  #  end
  #  puts o.to_json
  #end
end
