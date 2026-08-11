import unittest
from app.agents import ScriptDirector, MaterialCurator, RenderManager
from app.agents.script_director import ScriptDirectorAgent
from app.agents.material_curator import MaterialCuratorAgent
from app.agents.render_manager import RenderManagerAgent


class TestAgents(unittest.TestCase):

    def test_script_director_analyze_script_and_wpm(self):
        agent = ScriptDirector(default_language="es")
        metrics = agent.analyze_script("En una casa abandonada al final de la calle se escuchaban gritos...", voice_rate=0.88)
        self.assertEqual(metrics["word_count"], 12)
        self.assertEqual(metrics["voice_rate"], 0.88)
        self.assertIn("0:", metrics["estimated_time_formatted"])

    def test_material_curator_parallel_search(self):
        agent = MaterialCurator(max_workers=2)
        result = agent.curate_materials_for_script("Terror", "Una historia sobre apariciones", amount=3, aspect_ratio="9:16")
        self.assertEqual(result["aspect_ratio"], "9:16")
        self.assertEqual(result["count"], len(result["keywords"]))

    def test_render_manager_gpu_and_bgm_attenuation(self):
        agent = RenderManager(bgm_attenuation_db=-20.0)
        info = agent.get_render_environment_info()
        self.assertIn("codec", info)
        self.assertEqual(info["bgm_attenuation_db"], -20.0)
        self.assertIn("is_gpu_accelerated", info)

    def test_idea_generator_fallback(self):
        from app.agents import IdeaGenerator
        agent = IdeaGenerator(default_language="es")
        ideas = agent._fallback_ideas("Terror y Suspenso", count=3)
        self.assertEqual(len(ideas), 3)
        self.assertIn("title", ideas[0])
        self.assertIn("hook", ideas[0])


if __name__ == "__main__":
    unittest.main()
